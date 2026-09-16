from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "foodie_secret_key"


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "foodie.db")


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# CREATE CONTACT MESSAGE TABLE
# ==========================================

def create_contact_table():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            message_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Create table when app starts
create_contact_table()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# MENU
# ==========================================

@app.route("/menu")
def menu():
    return render_template("menu.html")


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# CONTACT
# ==========================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Check empty fields
        if not name or not email or not subject or not message:

            return render_template(
                "contact.html",
                error="Please fill all fields."
            )

        # Current date and time
        message_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Open database
        connection = get_db_connection()

        # Save message
        connection.execute(
            """
            INSERT INTO contact_messages
            (
                name,
                email,
                subject,
                message,
                message_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                subject,
                message,
                message_date
            )
        )

        # Save changes
        connection.commit()
        connection.close()

        # Show success message
        return render_template(
            "contact.html",
            success="✅ Your message has been sent successfully!"
        )

    return render_template("contact.html")


# ==========================================
# CONTACT MESSAGES
# ==========================================

@app.route("/messages")
def messages():

    connection = get_db_connection()

    messages = connection.execute(
        "SELECT * FROM contact_messages ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "messages.html",
        messages=messages
    )


# ==========================================
# ADD TO CART
# ==========================================

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    item_name = request.form.get("name")
    price = request.form.get("price")
    image = request.form.get("image")

    if not item_name or not price:

        return {
            "success": False,
            "message": "Invalid product data"
        }, 400

    try:

        price = float(price)

    except ValueError:

        return {
            "success": False,
            "message": "Invalid price"
        }, 400

    cart = session.get("cart", [])

    item_found = False

    for item in cart:

        if item["name"] == item_name:

            item["quantity"] += 1
            item_found = True

            break

    if not item_found:

        item = {
            "name": item_name,
            "price": price,
            "image": image,
            "quantity": 1
        }

        cart.append(item)

    session["cart"] = cart
    session.modified = True

    cart_count = sum(
        item["quantity"]
        for item in cart
    )

    return {
        "success": True,
        "message": item_name + " added to cart",
        "count": cart_count
    }


# ==========================================
# CART COUNT
# ==========================================

@app.route("/cart-count")
def cart_count():

    cart = session.get("cart", [])

    count = sum(
        item["quantity"]
        for item in cart
    )

    return {
        "count": count
    }


# ==========================================
# CART
# ==========================================

@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    subtotal = 0

    for item in cart_items:

        subtotal += (
            item["price"] *
            item["quantity"]
        )

    if subtotal > 0:

        delivery = 40

    else:

        delivery = 0

    total = subtotal + delivery

    return render_template(
        "cart.html",
        cart_items=cart_items,
        subtotal=subtotal,
        delivery=delivery,
        total=total
    )


# ==========================================
# REMOVE FROM CART
# ==========================================

@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):

        cart.pop(index)

    session["cart"] = cart
    session.modified = True

    return redirect(
        url_for("cart")
    )


# ==========================================
# CLEAR CART
# ==========================================

@app.route("/clear-cart")
def clear_cart():

    session["cart"] = []
    session.modified = True

    return redirect(
        url_for("cart")
    )


# ==========================================
# CHECKOUT
# ==========================================

@app.route("/checkout")
def checkout():

    cart_items = session.get("cart", [])

    subtotal = 0

    for item in cart_items:

        subtotal += (
            item["price"] *
            item["quantity"]
        )

    if subtotal > 0:

        delivery = 40

    else:

        delivery = 0

    total = subtotal + delivery

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        subtotal=subtotal,
        delivery=delivery,
        total=total
    )


# ==========================================
# PLACE ORDER
# ==========================================

@app.route("/place-order", methods=["POST"])
def place_order():

    customer_name = request.form.get("fullName")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")
    city = request.form.get("city")
    pincode = request.form.get("pincode")
    payment_method = request.form.get("payment")
    items = request.form.get("items")

    subtotal = request.form.get("subtotal")
    delivery = request.form.get("delivery")
    total = request.form.get("total")

    if subtotal is None:
        subtotal = 0

    if delivery is None:
        delivery = 0

    if total is None:
        total = 0

    order_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO orders (
            customer_name,
            phone,
            email,
            address,
            city,
            pincode,
            payment_method,
            items,
            subtotal,
            delivery,
            total,
            order_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            phone,
            email,
            address,
            city,
            pincode,
            payment_method,
            items,
            float(subtotal),
            float(delivery),
            float(total),
            order_date
        )
    )

    connection.commit()
    connection.close()

    session["cart"] = []
    session.modified = True

    return redirect(
        url_for("order_success")
    )


# ==========================================
# ORDER SUCCESS
# ==========================================

@app.route("/order-success")
def order_success():

    return render_template(
        "order-success.html"
    )


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)