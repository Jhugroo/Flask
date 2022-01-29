from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('first.html',show_categories=True)

@app.route('/cart')
def cart():
	return render_template('cart.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/detail')
def detail():
	return render_template('detail.html')

@app.route('/checkout')
def checkout():
	return render_template('checkout.html')

@app.route('/shop')
def shop():
	return render_template('shop.html')

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

