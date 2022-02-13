from math import prod
from flask import *
import requests
import string
import random
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
import stripe
# from selenium import webdriver as wd
# import chromedriver_binary

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/charge', methods=["POST"])
def charge():
    productCode = request.form.get('productCode')
    address = request.form.get('street_address')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM products where code = ?",(productCode,))
        product = cur.fetchone()
        customer = stripe.Customer.create(
			email='customer@example.com',
			source=request.form['stripeToken']
		)
        charge = stripe.Charge.create(
			customer=customer.id,
			amount=int(product[2])*100,
			currency='usd',
			description=product[1]
		)
        false=False
        list_of_cookies=[
		{
			"domain": ".amazon.com",
			"expirationDate": 1644925588.404523,
			"hostOnly": false,
			"httpOnly": false,
			"name": "i18n-prefs",
			"path": "/",
			"sameSite": "unspecified",
			"secure": false,
			"session": false,
			"storeId": "0",
			"value": "INR",
			"id": 1
		}]
        product_link=product[6]
		# amazon.login_cookie(cookies=list_of_cookies)
        # amazon.login(password='kok', email='kok@gmail.com')
        # amazon.buy(product_url=product_link)
        # amazon.select_payment_method(payment_method='Mauritius Commercial Bank')
        # amazon.fill_cvv(cvv='123')
        # print(amazon);
        # amazon.place_order()
        # wd = wd.Chrome()
        # wd.implicitly_wait(10)
        # wd.get('https://www.amazon.com/MEROKEETY-Popcorn-Batwing-Cardigan-Oversized/dp/B08C4VFDQC/ref=sr_1_1?keywords=cardigans&pd_rd_r=0d5667f7-cf42-47bc-a293-ac945c57021f&pd_rd_w=n6UEY&pd_rd_wg=nypok&pf_rd_p=bb27b743-d39d-4423-a18e-dd1d61011f4f&pf_rd_r=MVKNQDYWBS7KRXH26QZ9&qid=1644738540&s=fashion-womens-intl-ship&sr=1-1&th=1&psc=1')
        # add_to_cart_button = wd.find_element_by_xpath('//*[@id="add-to-cart-button"]')
        # add_to_cart_button.click()
        return render_template('charge.html', amount=charge,customer=customer)

@app.route('/uhh')
def uhhh():
	return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/')
def index():
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT *, name FROM products")
		categories = cur.fetchall()
	return render_template('front/index.html',show_categories=True, title = 'KOK main page',categories=categories)

@app.route('/about')
def about():
	return render_template('front/about.html')

@app.route('/blog')
def blog():
	return render_template('front/blog.html')

@app.route('/elements')
def elements():
	return render_template('front/elements.html')

@app.route('/blog-details')
def blog_details():
	return render_template('front/blog_details.html')

@app.route('/product', methods=["GET","POST"])
def product():
	with sqlite3.connect('database.db') as connection:
		cur = connection.cursor()
		cur.execute("SELECT * FROM categories")
		categories = cur.fetchall()
	name = request.form.get('name')
	code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
	thumbnail =request.files.get('thumbnail')
	if thumbnail and allowed_file(thumbnail.filename):
		filename = secure_filename(thumbnail.filename)
		code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
		thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], code +filename))
		thumbnail = filename
		thumbnailImage = code+thumbnail
		price = request.form.get('price')
		description =request.form.get('description')
		stock = request.form.get('oldprice')
		link = request.form.get('link')
		categoryId = request.form.get('category')
		with sqlite3.connect('database.db') as conn:
			cur = conn.cursor()
			cur.execute('INSERT INTO products (name, price, description, code, link, stock, thumbnailImage, categoryId) VALUES (?, ?, ?,?,? , ?, ?, ?)', (name, price, description, code, link, stock, thumbnailImage, categoryId))
			conn.commit()
	x = 0
	while x < 6:
		image =request.files.get('image'+str(x))
		x = x +1
		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], code +filename))
			imagename = filename
			imagehash = code+imagename
			with sqlite3.connect('database.db') as conn:
				cur = conn.cursor()
				cur.execute("SELECT * FROM products order by productId desc limit 1")
				productId = cur.fetchone()[0];
				cur.execute('INSERT INTO images (imagehash, productId) VALUES (?, ?)', (imagehash, productId))
				conn.commit()
	return render_template('front/admin/product.html', categories=categories)

@app.route('/category', methods=["GET","POST"])
def category():
	category = request.form.get('category')
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('INSERT INTO categories(name) VALUES (?)', (category,))
		conn.commit()
	return render_template('front/admin/category.html')

@app.route('/cart')
def cart():
	return render_template('front/cart.html', title = 'KOK cart page')

@app.route('/contact')
def contact():
	return render_template('front/contact.html', title = 'KOK contact page')

@app.route('/product_details/<code>')
def detail(code):
	with sqlite3.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT * FROM products where code = ?",(code,))
		product = cur.fetchone()
		cur.execute("SELECT * FROM images where productId = ?",(product[0],))
		images = cur.fetchall()
		return render_template('front/shop/product_details.html', title = 'KOK detail page',product=product, images= images,  key=stripe_keys['publishable_key'])

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

@app.route('/front')
def shion():
	return render_template('front/index.html', title = 'KOK shop page')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
if __name__ == '__main__':
	app.run()