from flask import Flask, jsonify, request
from flask_cors import CORS

from app import (
    get_customer,
    get_products,
    get_customer_orders,
    get_order_details,
    get_payment_details,
    get_order_summary,
    add_customer,
    update_customer_phone,
    delete_customer,
    authenticate_customer,
    get_dashboard_summary,
    get_category_counts,
    get_order_status_breakdown,
    get_low_stock_products,
    get_top_rated_products,
    checkout_order,
    get_customer_addresses
)

app = Flask(__name__)
CORS(app)  # allows index.html (opened as a file or from another port) to call this API


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return jsonify({
        "message": "Online Shopping Management System Backend is running!"
    })


# =========================================================
# GET CUSTOMER
# =========================================================

@app.route("/customer/<int:customer_id>", methods=["GET"])
def customer(customer_id):

    result = get_customer(customer_id)

    if result:
        return jsonify({
            "Customer_ID": result[0],
            "Name": result[1],
            "Email": result[2],
            "Phone": result[3]
        })

    return jsonify({
        "message": "Customer not found"
    }), 404


# =========================================================
# POST - LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("Email")
    password = data.get("Password")

    if not email or not password:
        return jsonify({
            "message": "Email and Password are required"
        }), 400

    result = authenticate_customer(email, password)

    if result:
        return jsonify({
            "message": "Login successful",
            "Customer_ID": result[0],
            "Name": result[1],
            "Email": result[2],
            "Phone": result[3]
        })

    return jsonify({
        "message": "Invalid email or password"
    }), 401


# =========================================================
# POST - ADD CUSTOMER
# =========================================================

@app.route("/customer", methods=["POST"])
def create_customer():

    data = request.get_json()

    customer_id = data["Customer_ID"]
    name = data["Name"]
    email = data["Email"]
    phone = data.get("Phone")
    password = data["Password"]

    result = add_customer(
        customer_id,
        name,
        email,
        phone,
        password
    )

    return jsonify({
        "message": result
    }), 201


# =========================================================
# GET ALL PRODUCTS
# =========================================================

@app.route("/products", methods=["GET"])
def products():

    result = get_products()

    product_list = []

    for product in result:
        product_list.append({
            "Product_ID": product[0],
            "Product_Name": product[1],
            "Category_Name": product[2],
            "Price": float(product[3]),
            "Stock_Quantity": product[4]
        })

    return jsonify(product_list)


# =========================================================
# GET CUSTOMER ORDERS
# =========================================================

@app.route("/orders/<int:customer_id>", methods=["GET"])
def customer_orders(customer_id):

    result = get_customer_orders(customer_id)

    order_list = []

    for order in result:
        order_list.append({
            "Order_ID": order[0],
            "Order_Date": str(order[1]),
            "Order_Status": order[2]
        })

    return jsonify(order_list)


# =========================================================
# GET ORDER DETAILS
# =========================================================

@app.route("/order/<int:order_id>", methods=["GET"])
def order_details(order_id):

    result = get_order_details(order_id)

    if not result:
        return jsonify({
            "message": "Order not found"
        }), 404

    order_list = []

    for row in result:
        order_list.append({
            "Order_ID": row[0],
            "Customer_Name": row[1],
            "Product_Name": row[2],
            "Quantity": row[3],
            "Unit_Price": float(row[4])
        })

    return jsonify(order_list)


# =========================================================
# GET PAYMENT DETAILS
# =========================================================

@app.route("/payment/<int:order_id>", methods=["GET"])
def payment_details(order_id):

    result = get_payment_details(order_id)

    if not result:
        return jsonify({
            "message": "Payment details not found"
        }), 404

    return jsonify({
        "Payment_ID": result[0],
        "Order_ID": result[1],
        "Payment_Method": result[2],
        "Payment_Status": result[3],
        "Amount": float(result[4]),
        "Payment_Date": str(result[5])
    })


# =========================================================
# GET COMPLETE ORDER SUMMARY
# =========================================================

@app.route("/order-summary/<int:order_id>", methods=["GET"])
def order_summary(order_id):

    result = get_order_summary(order_id)

    if not result:
        return jsonify({
            "message": "Order summary not found"
        }), 404

    summary_list = []

    for row in result:
        summary_list.append({
            "Order_ID": row[0],
            "Customer_Name": row[1],
            "Product_Name": row[2],
            "Quantity": row[3],
            "Unit_Price": float(row[4]),
            "Payment_Method": row[5],
            "Payment_Status": row[6],
            "Amount": float(row[7])
        })

    return jsonify(summary_list)


# =========================================================
# PUT - UPDATE CUSTOMER PHONE
# =========================================================

@app.route("/customer/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):

    data = request.get_json()

    phone = data["Phone"]

    result = update_customer_phone(
        customer_id,
        phone
    )

    return jsonify({
        "message": result
    })


# =========================================================
# DELETE - DELETE CUSTOMER
# =========================================================

@app.route("/customer/<int:customer_id>", methods=["DELETE"])
def remove_customer(customer_id):

    result = delete_customer(customer_id)

    return jsonify({
        "message": result
    })


# =========================================================
# GET - CUSTOMER'S PAST ADDRESSES
# =========================================================

@app.route("/addresses/<int:customer_id>", methods=["GET"])
def customer_addresses(customer_id):
    result = get_customer_addresses(customer_id)
    return jsonify([
        {
            "Address_ID": row[0],
            "House_No": row[1],
            "Street": row[2],
            "City": row[3],
            "State": row[4],
            "Pincode": row[5]
        }
        for row in result
    ])


# =========================================================
# POST - CHECKOUT (create order + order items + payment)
# =========================================================

@app.route("/checkout", methods=["POST"])
def checkout():

    data = request.get_json()

    customer_id = data.get("Customer_ID")
    address = data.get("Address")
    items = data.get("Items")
    payment_method = data.get("Payment_Method")

    if not customer_id:
        return jsonify({"message": "You must be logged in to checkout"}), 401

    if not address or not all(address.get(f) for f in ["House_No", "Street", "City", "State", "Pincode"]):
        return jsonify({"message": "A complete delivery address is required"}), 400

    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({"message": "Your cart is empty"}), 400

    if not payment_method:
        return jsonify({"message": "Please choose a payment method"}), 400

    try:
        result = checkout_order(customer_id, address, items, payment_method)
        return jsonify({
            "message": "Order placed successfully!",
            **result
        }), 201
    except Exception as e:
        return jsonify({
            "message": f"Checkout failed: {str(e)}"
        }), 500


# =========================================================
# DASHBOARD - SUMMARY
# =========================================================

@app.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    return jsonify(get_dashboard_summary())


# =========================================================
# DASHBOARD - PRODUCTS PER CATEGORY
# =========================================================

@app.route("/dashboard/category-counts", methods=["GET"])
def dashboard_category_counts():
    result = get_category_counts()
    return jsonify([
        {"Category_Name": row[0], "Product_Count": row[1]}
        for row in result
    ])


# =========================================================
# DASHBOARD - ORDERS PER STATUS
# =========================================================

@app.route("/dashboard/order-status", methods=["GET"])
def dashboard_order_status():
    result = get_order_status_breakdown()
    return jsonify([
        {"Order_Status": row[0], "Order_Count": row[1]}
        for row in result
    ])


# =========================================================
# DASHBOARD - LOW STOCK PRODUCTS
# =========================================================

@app.route("/dashboard/low-stock", methods=["GET"])
def dashboard_low_stock():
    threshold = request.args.get("threshold", default=10, type=int)
    result = get_low_stock_products(threshold)
    return jsonify([
        {"Product_Name": row[0], "Stock_Quantity": row[1]}
        for row in result
    ])


# =========================================================
# DASHBOARD - TOP RATED PRODUCTS
# =========================================================

@app.route("/dashboard/top-rated", methods=["GET"])
def dashboard_top_rated():
    limit = request.args.get("limit", default=5, type=int)
    result = get_top_rated_products(limit)
    return jsonify([
        {"Product_Name": row[0], "Avg_Rating": float(row[1]), "Review_Count": row[2]}
        for row in result
    ])


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)