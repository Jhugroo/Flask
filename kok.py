from flask import *
import string
import random
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'uytb878978uygfutBUUDR4564564523'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT *, name FROM products")
		categories = cur.fetchall()
	return render_template('front/homepage/index2.html',show_categories=True, title = 'KOK main page',categories=categories)

@app.route('/create', methods=["GET","POST"])
def create():
	name = request.form.get('name')
	msg = False
	if (name):
		with sqlite3.connect('database.db') as conn:
			cur = conn.cursor()
			cur.execute('INSERT INTO categories(name) VALUES (?)', (name,))
			conn.commit()
			msg = True
	return render_template('front/homepage/create.html', msg=msg)

@app.route('/product', methods=["GET","POST"])
def product():
	image = request.files.get('image')
	name = request.form.get('name')
	if(image):
		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
		price = 324234
		description = "sdfdsfwsefeswfsfsfe"
		stock = 23
		categoryId = 14
		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], res+filename))
			imagename = filename
			imagehash = res+imagename
			with sqlite3.connect('database.db') as conn:
				cur = conn.cursor()
				cur.execute('INSERT INTO products (name, price, description, image, res, stock, categoryId) VALUES (?, ?, ?, ?,?, ?, ?)', (name, price, description, imagename, imagehash, stock, categoryId))
				conn.commit()
	return render_template('front/homepage/create.html')

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
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT *, name FROM products")
		products = cur.fetchall()
	return render_template('front/shop/shop.html', title = 'KOK shop page', products=products)

@app.route('/admin')
def admin():
	return render_template('admin/index.html')

@app.route('/shion')
def shion():
	return render_template('shion/index.html', title = 'KOK shop page')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
if __name__ == '__main__':
	app.run()