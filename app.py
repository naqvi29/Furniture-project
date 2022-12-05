from flask import Flask, render_template ,request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'furniture'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL(app)
 

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    return render_template("index.html",home=True,categories=categories)

@app.route("/contact")
def contact():
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    return render_template("contact.html",contact=True,categories=categories)

@app.route("/product-details/<int:id>")
def product_details(id):
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from products where id=%s;',[id])    
    product = cursor.fetchone()
    return render_template("product-details.html",shop=True,categories=categories,product=product)

@app.route("/shop")
def shop():
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from brands;')    
    brands = cursor.fetchall()
    cursor.execute('Select * from products;')    
    products = cursor.fetchall()
    return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products)

@app.route("/category/<int:id>")
def category(id):
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from brands;')    
    brands = cursor.fetchall()
    cursor.execute('Select * from categories where id=%s;',[id])    
    selected = cursor.fetchone()
    cursor.execute('Select * from products where category_id=%s;',[id])    
    products = cursor.fetchall()
    return render_template("shop.html",shop=True,categories=categories,selected=selected,brands=brands,products=products)

@app.route("/apply-brand/<string:json>")
def apply_brand(json):
    print(json)
    brand_ids = "("+json+")"
    print(brand_ids)
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from brands;')    
    brands = cursor.fetchall()
    cursor.execute('Select * from products where brand_id in '+brand_ids)
    products = cursor.fetchall()
    return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products)

@app.route("/apply-price/<string:minamount>/<string:maxamount>")
def apply_price(minamount,maxamount):
    print(minamount, maxamount)
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from brands;')    
    brands = cursor.fetchall()
    cursor.execute('SELECT * FROM products where price >= %s and price <= %s;',(minamount,maxamount))
    products = cursor.fetchall()
    return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products)

if __name__ =="__main__":
    app.run(debug=True)