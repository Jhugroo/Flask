from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('layout.html')

@app.route('/pti-bebe')
def bebe():
	return 'hi pti pti'

@app.route('/user/<name>/<name2>')
def user(name,name2):
    return render_template('first.html', name=name,name2=name2)

@app.route('/pti-bebes-page')
def pti():
   	return 'hi choco chip'

@app.route('/new-page')
def newpage():
   	return 'hi choco chip'

if __name__ == '__main__':
	app.run()

