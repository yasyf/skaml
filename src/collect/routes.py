from flask import render_template, session, jsonify, request, send_file
from app import app
from helpers.mongo import db
from helpers.transform import transform
import uuid, io
import numpy as np

@app.before_request
def preprocess_request():
  if not session.get('id'):
    session['id'] = str(uuid.uuid4())

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_view():
  obj = {'words': request.json['words'], 'id': session['id']}
  db.sessions.update({'id': session['id']},obj, upsert=True)
  return jsonify({'status': 'success'})

@app.route('/admin')
def admin_view():
  return render_template('admin.html', sessions=db.sessions.find({}))

@app.route('/export/<id>')
def export_view(id):
  obj = db.sessions.find_one({'id': session['id']})
  X, Y = transform(obj)
  output = io.BytesIO()
  np.savez_compressed(output, X=X, Y=Y)
  output.seek(0)
  return send_file(output, as_attachment=True, attachment_filename='export.npz')
