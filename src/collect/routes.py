from flask import render_template
from app import app

@app.route('/')
def index_view():
  return render_template('index.html')
