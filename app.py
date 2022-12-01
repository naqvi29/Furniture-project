from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/product-details")
def product_details():
    return render_template("product-details.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

if __name__ =="__main__":
    app.run(debug=True)