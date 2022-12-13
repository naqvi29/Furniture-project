from flask import Flask, render_template ,request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import os
import json
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
    if 'loggedin' in session:
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("index.html",home=True,categories=categories,loggedin=True,username=session['name'],cart_items=cart_items, total=total)
    else:
        return render_template("index.html",home=True,categories=categories)


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password") 
        cursor = mysql.connection.cursor()
        cursor.execute('Select * from users where email=%s;',[email])    
        account = cursor.fetchone()
        if not account:
            return render_template("login.html",error="Invalid Email!")
        if account['password'] != password:
            return render_template("login.html",error="Invalid Password!")
        session['loggedin'] = True
        session['userid'] = str(account["id"])
        session['name'] = account["name"]
        session['email'] = account["email"]
        return redirect(url_for("index"))
        
    return render_template("login.html")


@app.route("/logout")
def logout():
    try:
        if 'loggedin' in session:
            session.pop('loggedin', None)
            session.pop('userid', None)
            session.pop('name', None)
            session.pop('email', None)
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confpassword = request.form.get("confpassword")
        if password != confpassword:
            return render_template("register.html",error="Passwords dont match!") 
        cursor = mysql.connection.cursor()
        cursor.execute('Select * from users where email=%s;',[email])    
        exist = cursor.fetchone()
        if exist:
            return render_template("register.html",error="Email Already Exists") 
        cursor.execute('INSERT INTO users (email,name,password) VALUES (%s,%s,%s);',[email,fullname,password])
        mysql.connection.commit()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO messages (name,email,message) VALUES (%s,%s,%s);',[name,email,message])
        mysql.connection.commit()
        cursor = mysql.connection.cursor()
        cursor.execute('Select * from categories;')    
        categories = cursor.fetchall()
        if 'loggedin' in session:
            cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
            cart_items = cursor.fetchall()
            total = 0
            for i in cart_items:
                x = i['price'] * i['qty']
                total = total + x
            return render_template("contact.html",contact=True,categories=categories, send=True,loggedin=True,cart_items=cart_items,total=total)          
        else:
            return render_template("contact.html",contact=True,categories=categories, send=True)
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    if 'loggedin' in session:
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("contact.html",contact=True,categories=categories,loggedin=True,username=session['name'],cart_items=cart_items,total=total)
    else:
        return render_template("contact.html",contact=True,categories=categories)

@app.route("/product-details/<int:id>")
def product_details(id):
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from products where id=%s;',[id])    
    product = cursor.fetchone()
    colors = []
    color_ids = json.loads(product['color_ids'])
    for i in color_ids:
        cursor.execute('Select * from colors where id=%s;',[i])
        color = cursor.fetchone()
        colors.append({"id":color['id'],"name":color['name'],"code":color['code']})
        
    sizes = []
    size_ids = json.loads(product['sizes'])
    for i in size_ids:
        cursor.execute('Select * from sizes where id=%s;',[i])
        size = cursor.fetchone()
        sizes.append({"id":size['id'],"name":size['name']})


    if 'loggedin' in session:
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("product-details.html",shop=True,categories=categories,product=product,loggedin=True,username=session['name'],colors=colors,sizes=sizes,cart_items=cart_items,total=total)
    else:
        return render_template("product-details.html",shop=True,categories=categories,product=product,colors=colors,sizes=sizes)

@app.route("/shop")
def shop():
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from categories;')    
    categories = cursor.fetchall()
    cursor.execute('Select * from brands;')    
    brands = cursor.fetchall()
    cursor.execute('Select * from products;')    
    products = cursor.fetchall()
    cursor.execute('Select * from colors;')    
    colors = cursor.fetchall()
    cursor.execute('Select * from sizes;')    
    sizes = cursor.fetchall()
    if 'loggedin' in session:
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products,colors=colors,sizes=sizes,loggedin=True,username=session['name'],cart_items=cart_items,total=total)
    else:
        return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products,colors=colors,sizes=sizes)

@app.route("/cart")
def cart():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("cart.html",cart_items=cart_items,total=total)
    else:
        return redirect(url_for("login"))

@app.route("/add-to-cart-route",methods=['GET','POST'])
def add_to_cart_route():
    if request.method == "POST":
        if 'loggedin' in session:
            data = request.json
            product_id = int(data['product_id'])
            try:
                color_id = int(data['color_id'])
            except Exception:
                color_id = None
            try:
                size_id = int(data['size_id'])
            except Exception:
                size_id = None
            try:
                qty = int(data['qty'])
            except Exception:
                qty = 1
            # fetch product details 
            
            cursor = mysql.connection.cursor()
            cursor.execute('Select * from products where id=%s;',[product_id])    
            product_details = cursor.fetchone()
            print("product is : ",product_details)

            # check if the product already in cart:
            cursor = mysql.connection.cursor()
            cursor.execute('Select * from cart_items where user_id=%s and product_id=%s;',[session['userid'],product_id])    
            exist = cursor.fetchone()
            if exist:
                prevQty = int(exist['qty'])
                UpdatedQty = prevQty+1
                cursor.execute('UPDATE cart_items SET qty=%s WHERE user_id=%s and product_id=%s;',[UpdatedQty,session['userid'],product_id])
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO cart_items (user_id,product_id,product_name,qty,price,image,size_id,color_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);',[session['userid'],product_id,product_details['name'],qty,float(product_details['price']),product_details['image'],size_id,color_id])
                mysql.connection.commit()
            return "True"

        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



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
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
        cart_items = cursor.fetchall()
        total = 0
        for i in cart_items:
            x = i['price'] * i['qty']
            total = total + x
        return render_template("shop.html",shop=True,categories=categories,selected=selected,brands=brands,products=products,loggedin=True,username=session['name'],cart_items=cart_items,total=total)
    else:
        return render_template("shop.html",shop=True,categories=categories,selected=selected,brands=brands,products=products)

@app.route("/apply-filter",methods=['POST'])
def apply_filter():
    if request.method=='POST':
        brands = request.form.getlist('brand-checkbox')
        colors = request.form.getlist('color-checkbox')
        min_amount = request.form.getlist('minamount')[0]
        max_amount = request.form.getlist('maxamount')[0]
        size = request.form['size-radio']
        brand_ids = []
        for i in brands:
            brand_ids.append(int(i))
        brand_json = json.dumps(brand_ids)
        brand_ids = brand_json.replace("[","(")
        brand_ids = brand_ids.replace("]",")")
        color_ids = []
        cursor = mysql.connection.cursor()
        product_ids_for_colors = []
        for i in colors:
            color_ids.append(int(i))
            cursor.execute('Select product_ids from colors where id =%s',[i])
            product_id = cursor.fetchone()['product_ids']
            try:
                for j in json.loads(product_id):
                    product_ids_for_colors.append(j)
            except Exception as e:
                print(e)
        product_ids_for_colors = list(dict.fromkeys(product_ids_for_colors))
            
        # product_ids_for_colors = json.dumps(product_ids_for_colors)
        # product_ids_for_colors = product_ids_for_colors.replace("[","(")
        # product_ids_for_colors = product_ids_for_colors.replace("]",")")

        cursor.execute('Select product_ids from sizes where id=%s;',[size])
        product_ids_for_sizes = json.loads(cursor.fetchone()['product_ids'])
        product_ids_for_sizes = list(product_ids_for_sizes)
        # product_ids_for_sizes = product_ids_for_sizes.replace("[","(")
        # product_ids_for_sizes = product_ids_for_sizes.replace("]",")")

        p_ids = product_ids_for_colors + product_ids_for_sizes
        p_ids = list(dict.fromkeys(p_ids))
        p_ids = json.dumps(p_ids)
        p_ids = p_ids.replace("[","(")
        p_ids = p_ids.replace("]",")")

        cursor = mysql.connection.cursor()
        cursor.execute('Select * from products where brand_id in '+brand_ids+' and id in '+p_ids+' and price >= '+min_amount+' and price <= '+max_amount)
        # cursor.execute('Select * from products where brand_id in %s and id in %s',[brand_ids,product_ids_for_colors])
        products = cursor.fetchall()

        cursor.execute('Select * from categories;')    
        categories = cursor.fetchall()
        cursor.execute('Select * from brands;')    
        brands = cursor.fetchall()
        cursor.execute('Select * from colors;')    
        colors = cursor.fetchall()
        cursor.execute('Select * from sizes;')    
        sizes = cursor.fetchall()
        
        if 'loggedin' in session:
            cursor = mysql.connection.cursor()
            cursor.execute('Select * from cart_items where user_id=%s',[session['userid']])
            cart_items = cursor.fetchall()
            total = 0
            for i in cart_items:
                x = i['price'] * i['qty']
                total = total + x
            return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products,loggedin=True,username=session['name'],colors=colors,sizes=sizes,cart_items=cart_items,total=total)
        else:
            return render_template("shop.html",shop=True,categories=categories,brands=brands,products=products,colors=colors,sizes=sizes)
if __name__ =="__main__":
    app.run(debug=True)