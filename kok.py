from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('front/homepage/index.html',show_categories=True, title = 'KOK main page')

@app.route('/cart')
def cart():
	return render_template('front/cart.html', title = 'KOK cart page')

@app.route('/contact')
def contact():
	return render_template('front/contact.html', title = 'KOK contact page')

@app.route('/detail')
def detail():
	return render_template('front/shop/detail.html', title = 'KOK detail page')

@app.route('/checkout')
def checkout():
	return render_template('front/checkout.html')

@app.route('/shop')
def shop():
	return render_template('front/shop/shop.html', title = 'KOK shop page')

@app.route('/admin')
def admin():
	return render_template('admin/index.html')

@app.route('/shion')
def shion():
	return render_template('shion/index.html', title = 'KOK shop page')
if __name__ == '__main__':
	app.run()