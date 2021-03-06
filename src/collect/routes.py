from flask import render_template, session, jsonify, request, send_file, redirect
from app import app
from helpers.mongo import db
from helpers.transform import transform, encode_chars, filter_valid
from helpers.learn import string_delay, chars_delay, evaluate
import uuid, io, os
import numpy as np

@app.before_request
def preprocess_request():
  if request.args.get('session_id'):
    session['id'] = request.args['session_id']
  if not session.get('id'):
    session['id'] = str(uuid.uuid4())

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/login')
def login_view():
  return render_template('login.html')

@app.route('/client')
def client_view():
  return redirect('https://chrome.google.com/webstore/detail/' + os.environ['APPID'])

@app.route('/words', methods=['POST'])
def words_view():
  obj = {'words': request.json['words'], 'id': session['id'], 'name': request.args.get('name')}
  db.sessions.update({'id': session['id']},obj, upsert=True)
  return jsonify({'status': 'success'})

@app.route('/admin')
def admin_view():
  return render_template('admin.html', sessions=db.sessions.find({}))

@app.route('/admin/<id>')
def detail_view(id):
  obj = db.sessions.find_one({'id': id})
  words = filter_valid(obj)
  _, delays, holds = transform(obj)
  return render_template('details.html', id=id, words=words, holds=holds, delays=delays, name=obj.get('name'))

@app.route('/means/<id>/<password>')
def string_mean_view(id, password):
  obj = db.sessions.find_one({'id': id})
  delays = string_delay(obj, password)
  return jsonify({'delays': delays})

@app.route('/means/<id>', methods=['POST'])
def chars_mean_view(id):
  obj = db.sessions.find_one({'id': id})
  delays = chars_delay(obj, request.json['word']['characters'])
  return jsonify({'delays': delays})

@app.route('/evaluate', methods=['POST'])
def evaluate_view():
  success, likelihood = evaluate(request.json['username'], request.json['password'])
  return jsonify({'success': success, 'likelihood': likelihood})

@app.route('/encode', methods=['POST'])
def encode_view():
  return jsonify({'encoded': encode_chars(request.json['word']['characters'])})

@app.route('/export/<id>')
def export_view(id):
  obj = db.sessions.find_one({'id': id})
  X, Y, Z = transform(obj)
  output = io.BytesIO()
  np.savez_compressed(output, X=X, Y=Y, Z=Z)
  output.seek(0)
  return send_file(output, as_attachment=True, attachment_filename='{}.npz'.format(id))
