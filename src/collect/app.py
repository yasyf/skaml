from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SK')
app.wsgi_app = ProxyFix(app.wsgi_app)
dev = os.environ.get('DEV') == 'true'

from routes import *

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT') or 5000), debug=dev)
