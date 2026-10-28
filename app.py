from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# CREATE - Add Customer
# =========================================================

def add_customer(customer_id, name, email, phone, password):
    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    query = """
    INSERT INTO CUSTOMER
    (Customer_ID, Name, Email, Phone, Password)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (customer_id, name, email, phone, hashed_password)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return "Customer added successfully!"


# =========================================================
# READ - Get Customer
# =========================================================

def get_customer(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT Customer_ID, Name, Email, Phone
    FROM CUSTOMER
    WHERE Customer_ID = %s
    """

    cursor.execute(query, (customer_id,))

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return customer


# =========================================================
# READ - Authenticate Customer (Login)
# =========================================================

def authenticate_customer(email, password):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT Customer_ID, Name, Email, Phone, Password
    FROM CUSTOMER
    WHERE Email = %s
    """

    cursor.execute(query, (email,))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row and check_password_hash(row[4], password):
        # Return only the public fields, never the password hash
        return row[0], row[1], row[2], row[3]

    return None


# =========================================================
# READ - Get All Products
# =========================================================

def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        p.Product_ID,
        p.Product_Name,
        c.Category_Name,
        p.Price,
        p.Stock_Quantity
    FROM PRODUCT p
    JOIN CATEGORY c
        ON p.Category_ID = c.Category_ID
    ORDER BY p.Product_ID
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


# =========================================================
# UPDATE - Update Customer Phone
# =========================================================

def update_customer_phone(customer_id, phone):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE CUSTOMER
    SET Phone = %s
    WHERE Customer_ID = %s
    """

    cursor.execute(query, (phone, customer_id))
    connection.commit()

    cursor.close()
    connection.close()

    return "Customer updated successfully!"


# =========================================================
# DELETE - Delete Customer
# =========================================================

def delete_customer(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM CUSTOMER
    WHERE Customer_ID = %s
    """

    cursor.execute(query, (customer_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return "Customer deleted successfully!"


# =========================================================
# READ - Get Customer Orders
# =========================================================

def get_customer_orders(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        o.Order_ID,
        o.Order_Date,
        o.Order_Status
    FROM ORDERS o
    WHERE o.Customer_ID = %s
    ORDER BY o.Order_ID
    """

    cursor.execute(query, (customer_id,))

    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return orders


# =========================================================
# READ - Get Order Details
# =========================================================

def get_order_details(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        o.Order_ID,
        c.Name AS Customer_Name,
        p.Product_Name,
        oi.Quantity,
        oi.Unit_Price
    FROM ORDERS o
    JOIN CUSTOMER c
        ON o.Customer_ID = c.Customer_ID
    JOIN ORDER_ITEM oi
        ON o.Order_ID = oi.Order_ID
    JOIN PRODUCT p
        ON oi.Product_ID = p.Product_ID
    WHERE o.Order_ID = %s
    """

    cursor.execute(query, (order_id,))

    details = cursor.fetchall()

    cursor.close()
    connection.close()

    return details


# =========================================================
# READ - Get Payment Details
# =========================================================

def get_payment_details(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        pay.Payment_ID,
        pay.Order_ID,
        pay.Payment_Method,
        pay.Payment_Status,
        pay.Amount,
        pay.Payment_Date
    FROM PAYMENT pay
    WHERE pay.Order_ID = %s
    """

    cursor.execute(query, (order_id,))

    payment = cursor.fetchone()

    cursor.close()
    connection.close()

    return payment


# =========================================================
# CREATE - Add Review
# =========================================================

def add_review(
    review_id,
    customer_id,
    product_id,
    rating,
    review_text,
    review_date
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO REVIEW
    (Review_ID, Customer_ID, Product_ID, Rating, Review_Text, Review_Date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        review_id,
        customer_id,
        product_id,
        rating,
        review_text,
        review_date
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return "Review added successfully!"


# =========================================================
# READ - Get Complete Order Summary
# =========================================================

def get_order_summary(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        o.Order_ID,
        c.Name AS Customer_Name,
        p.Product_Name,
        oi.Quantity,
        oi.Unit_Price,
        pay.Payment_Method,
        pay.Payment_Status,
        pay.Amount
    FROM ORDERS o
    JOIN CUSTOMER c
        ON o.Customer_ID = c.Customer_ID
    JOIN ORDER_ITEM oi
        ON o.Order_ID = oi.Order_ID
    JOIN PRODUCT p
        ON oi.Product_ID = p.Product_ID
    JOIN PAYMENT pay
        ON o.Order_ID = pay.Order_ID
    WHERE o.Order_ID = %s
    """

    cursor.execute(query, (order_id,))

    summary = cursor.fetchall()

    cursor.close()
    connection.close()

    return summary


# =========================================================
# UPDATE - Update Order Status
# =========================================================

def update_order_status(order_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE ORDERS
    SET Order_Status = %s
    WHERE Order_ID = %s
    """

    cursor.execute(query, (status, order_id))
    connection.commit()

    cursor.close()
    connection.close()

    return "Order status updated successfully!"


# =========================================================
# UPDATE - Update Payment Status
# =========================================================

def update_payment_status(payment_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE PAYMENT
    SET Payment_Status = %s
    WHERE Payment_ID = %s
    """

    cursor.execute(query, (status, payment_id))
    connection.commit()

    cursor.close()
    connection.close()

    return "Payment status updated successfully!"


# =========================================================
# TEST BACKEND
# =========================================================

# =========================================================
# DASHBOARD - Summary Counts and Revenue
# =========================================================

def get_dashboard_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM CUSTOMER")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ORDERS")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM PRODUCT")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(Amount), 0) FROM PAYMENT")
    total_revenue = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(Stock_Quantity), 0) FROM PRODUCT")
    total_stock_units = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_revenue": float(total_revenue),
        "total_stock_units": total_stock_units
    }


# =========================================================
# DASHBOARD - Product Count per Category (GROUP BY)
# =========================================================

def get_category_counts():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        c.Category_Name,
        COUNT(p.Product_ID) AS Product_Count
    FROM CATEGORY c
    LEFT JOIN PRODUCT p
        ON c.Category_ID = p.Category_ID
    GROUP BY c.Category_Name
    ORDER BY Product_Count DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# =========================================================
# DASHBOARD - Order Count per Status (GROUP BY)
# =========================================================

def get_order_status_breakdown():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT Order_Status, COUNT(*) AS Order_Count
    FROM ORDERS
    GROUP BY Order_Status
    ORDER BY Order_Count DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# =========================================================
# DASHBOARD - Low Stock Products
# =========================================================

def get_low_stock_products(threshold=10):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT Product_Name, Stock_Quantity
    FROM PRODUCT
    WHERE Stock_Quantity < %s
    ORDER BY Stock_Quantity ASC
    """

    cursor.execute(query, (threshold,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# =========================================================
# DASHBOARD - Top Rated Products (JOIN + GROUP BY + HAVING)
# =========================================================

def get_top_rated_products(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        p.Product_Name,
        ROUND(AVG(r.Rating), 2) AS Avg_Rating,
        COUNT(r.Review_ID) AS Review_Count
    FROM REVIEW r
    JOIN PRODUCT p
        ON r.Product_ID = p.Product_ID
    GROUP BY p.Product_ID, p.Product_Name
    HAVING COUNT(r.Review_ID) > 0
    ORDER BY Avg_Rating DESC
    LIMIT %s
    """

    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# =========================================================
# CHECKOUT - Create Address + Order + Order Items + Payment
# =========================================================

def checkout_order(customer_id, address, items, payment_method):
    """
    address: dict with House_No, Street, City, State, Pincode
    items: list of dicts with Product_ID, Quantity, Unit_Price
    Runs everything in a single transaction so a failure partway
    through does not leave a half-created order in the database.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # 1. Create a new delivery address for this order
        cursor.execute("SELECT COALESCE(MAX(Address_ID), 0) + 1 FROM ADDRESS")
        address_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO ADDRESS
            (Address_ID, Customer_ID, House_No, Street, City, State, Pincode)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            address_id, customer_id,
            address.get("House_No"), address.get("Street"),
            address.get("City"), address.get("State"), address.get("Pincode")
        ))

        # 2. Create the order
        cursor.execute("SELECT COALESCE(MAX(Order_ID), 0) + 1 FROM ORDERS")
        order_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO ORDERS (Order_ID, Customer_ID, Address_ID, Order_Date, Order_Status)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (order_id, customer_id, address_id, "Processing"))

        # 3. Create one ORDER_ITEM row per cart item, and reduce stock
        total_amount = 0
        for item in items:
            quantity = item["Quantity"]
            unit_price = item["Unit_Price"]
            total_amount += quantity * unit_price

            cursor.execute("""
                INSERT INTO ORDER_ITEM (Order_ID, Product_ID, Quantity, Unit_Price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item["Product_ID"], quantity, unit_price))

            cursor.execute("""
                UPDATE PRODUCT
                SET Stock_Quantity = GREATEST(Stock_Quantity - %s, 0)
                WHERE Product_ID = %s
            """, (quantity, item["Product_ID"]))

        # 4. Create the payment record
        cursor.execute("SELECT COALESCE(MAX(Payment_ID), 0) + 1 FROM PAYMENT")
        payment_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PAYMENT (Payment_ID, Order_ID, Payment_Date, Payment_Method, Payment_Status, Amount)
            VALUES (%s, %s, CURDATE(), %s, %s, %s)
        """, (payment_id, order_id, payment_method, "Success", total_amount))

        connection.commit()

    except Exception:
        connection.rollback()
        cursor.close()
        connection.close()
        raise

    cursor.close()
    connection.close()

    return {
        "Order_ID": order_id,
        "Address_ID": address_id,
        "Payment_ID": payment_id,
        "Total_Amount": float(total_amount)
    }


# =========================================================
# CHECKOUT - Get Addresses for a Customer (for displaying past orders)
# =========================================================

def get_customer_addresses(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT Address_ID, House_No, Street, City, State, Pincode
    FROM ADDRESS
    WHERE Customer_ID = %s
    ORDER BY Address_ID
    """

    cursor.execute(query, (customer_id,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


if __name__ == "__main__":

    print("Online Shopping Management System")
    print("----------------------------------")

    # -----------------------------------------------------
    # Products
    # -----------------------------------------------------

    print("\nProducts:")

    products = get_products()

    for product in products:
        print(product)

    # -----------------------------------------------------
    # Customer Orders
    # -----------------------------------------------------

    print("\nOrders of Customer 101:")

    orders = get_customer_orders(101)

    for order in orders:
        print(order)

    # -----------------------------------------------------
    # Order Details
    # -----------------------------------------------------

    print("\nDetails of Order 501:")

    details = get_order_details(501)

    for detail in details:
        print(detail)

    # -----------------------------------------------------
    # Payment Details
    # -----------------------------------------------------

    print("\nPayment Details for Order 501:")

    payment = get_payment_details(501)

    print(payment)

    # -----------------------------------------------------
    # Complete Order Summary
    # -----------------------------------------------------

    print("\nComplete Order Summary for Order 501:")

    summary = get_order_summary(501)

    for row in summary:
        print(row)