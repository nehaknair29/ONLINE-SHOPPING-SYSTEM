# ShopNest — Online Shopping Management System

ShopNest is a database-backed online shopping system built with Python, Flask, MySQL, HTML, CSS, and JavaScript. It includes a customer-facing shopping interface and an admin dashboard for viewing store and inventory summaries.

> **Project status:** This repository contains the application code. A MySQL database with the required tables and data must be configured separately before the application can run.

## Features

### Customer shopping interface
- Browse products and filter them by category.
- Search for products.
- Log in using an email address and password.
- Add products to a shopping cart and adjust quantities.
- Submit an order with a delivery address and selected payment method.
- View an order confirmation after checkout.

### Backend and database
- Flask API endpoints for customers, products, orders, order details, payment records, and delivery addresses.
- MySQL database connectivity.
- Customer creation and authentication.
- Password hashing and password-hash verification using Werkzeug.
- Checkout workflow that records an address, order, order items, and a payment record in a database transaction.
- Customer phone updates and customer deletion endpoints.

### Admin dashboard
- Summary cards for customers, orders, products, revenue, and stock units.
- Product counts by category.
- Order counts by status.
- Low-stock product alerts.
- Top-rated products and review counts.
- Manual refresh and automatic dashboard refresh.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, Flask-CORS
- **Database:** MySQL
- **Database connector:** `mysql-connector-python`
- **Password security:** Werkzeug password hashing utilities

## Project Structure

```text
final/
├── api.py
├── app.py
├── database.py
├── migrate_hash_passwords.py
├── index.html
├── dashboard.html
├── README.md
├── requirements.txt
└── .gitignore
```

- `index.html` — customer-facing ShopNest shopping interface.
- `dashboard.html` — admin dashboard interface.
- `api.py` — Flask API routes used by the frontend.
- `app.py` — database operations and application logic.
- `database.py` — MySQL connection configuration.
- `migrate_hash_passwords.py` — one-time utility for converting existing plain-text customer passwords to Werkzeug password hashes.

## Prerequisites

Install the following before running the project:

- Python 3
- MySQL Server
- Git (optional, for cloning the repository)
- A browser

## Setup

### 1. Get the project files

Clone this repository after it has been uploaded, or download the project as a ZIP file from GitHub.

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

After creating `requirements.txt`, run:

```powershell
python -m pip install -r requirements.txt
```

The project requires these Python packages:

```powershell
python -m pip install Flask Flask-Cors mysql-connector-python Werkzeug
```

### 4. Configure MySQL

1. Start MySQL Server.
2. Create a MySQL database named `onlineshoppingsystem`, or update the database configuration to use your chosen database name.
3. Create and populate all tables required by the application.
4. Configure the database host, username, and password in `database.py` using your own local credentials.

**Database schema note:** The project files listed here do not include a SQL schema or seed-data file. The required tables and any sample data must be supplied separately for the application to work.

**Security note:** Never commit database passwords or other credentials to a public repository. Before publishing, remove any hard-coded password from `database.py` and use environment variables or another secure local configuration method. If a real password has already been committed or exposed, change it.

### 5. Run the Flask API

From the project directory, with the virtual environment activated, run:

```powershell
python api.py
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

The frontend files currently use this local API address. If you change the API host or port, update the `API_BASE` value in `index.html` and `dashboard.html` accordingly.

### 6. Open the frontend

With the API running, open `index.html` in your browser to use the shopping interface.

Open `dashboard.html` in your browser to view the admin dashboard.

Both pages request data from the local Flask API, so the backend and MySQL database must be running for dynamic content to load.

## API Overview

The Flask API includes routes for:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Check that the API is running |
| `GET` | `/customer/<customer_id>` | Retrieve a customer |
| `POST` | `/login` | Authenticate a customer |
| `POST` | `/customer` | Create a customer |
| `GET` | `/products` | Retrieve products |
| `GET` | `/orders/<customer_id>` | Retrieve a customer's orders |
| `GET` | `/order/<order_id>` | Retrieve order details |
| `GET` | `/payment/<order_id>` | Retrieve payment-record details |
| `GET` | `/order-summary/<order_id>` | Retrieve an order summary |
| `PUT` | `/customer/<customer_id>` | Update a customer's phone number |
| `DELETE` | `/customer/<customer_id>` | Delete a customer |
| `GET` | `/addresses/<customer_id>` | Retrieve a customer's saved addresses |
| `POST` | `/checkout` | Create checkout records |
| `GET` | `/dashboard/summary` | Retrieve dashboard summary metrics |
| `GET` | `/dashboard/category-counts` | Retrieve product counts by category |
| `GET` | `/dashboard/order-status` | Retrieve order counts by status |
| `GET` | `/dashboard/low-stock` | Retrieve low-stock products |
| `GET` | `/dashboard/top-rated` | Retrieve top-rated products |

## Payment Note

The application records a selected payment method and creates a payment record in MySQL during checkout. The current code does **not** integrate a real payment gateway, so the payment record should not be interpreted as confirmation that money was actually collected.

## Password Migration Utility

`migrate_hash_passwords.py` is intended to be run once against an existing database to hash customer passwords that are still stored in plain text.

Before using it:
- Back up the database.
- Confirm that the database connection points to the intended database.
- Run it only when needed for an existing dataset.

Do not run migration scripts against production data without reviewing and testing them first.

## Security and Limitations

- Use environment variables or a secure local configuration for database credentials.
- Do not upload real customer data, database dumps, passwords, or secret files.
- The application is configured for local development; review authentication, authorization, input validation, error handling, and deployment settings before production use.
- `api.py` currently starts Flask with debug mode enabled. Disable debug mode before deploying to a public server.
- A separate SQL schema/seed file would make setup easier for other developers.

## Future Improvements

- Add a SQL schema and sample-data script for easier setup.
- Move database credentials to environment variables.
- Integrate a real payment gateway in test mode.
- Add stronger authorization for admin-only operations.
- Add automated tests and clearer error handling.
- Deploy the frontend and backend to a hosted environment.

## Author

Created as a database management systems project.
