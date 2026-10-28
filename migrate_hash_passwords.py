"""
One-time migration: re-hash every existing plain-text password in the
CUSTOMER table so they work with the new authenticate_customer() / login
system, which expects Werkzeug password hashes.

Safe to run once. Running it a second time is harmless but unnecessary —
it skips rows whose Password column is already a recognized hash format.

Usage:
    python migrate_hash_passwords.py
"""

from database import get_connection
from werkzeug.security import generate_password_hash

# Werkzeug hashes always start with one of these method prefixes.
HASH_PREFIXES = ("scrypt:", "pbkdf2:")


def is_already_hashed(value):
    return isinstance(value, str) and value.startswith(HASH_PREFIXES)


def migrate():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Customer_ID, Password FROM CUSTOMER")
    rows = cursor.fetchall()

    updated = 0
    skipped = 0

    for customer_id, password in rows:
        if is_already_hashed(password):
            skipped += 1
            continue

        new_hash = generate_password_hash(password)

        update_cursor = connection.cursor()
        update_cursor.execute(
            "UPDATE CUSTOMER SET Password = %s WHERE Customer_ID = %s",
            (new_hash, customer_id)
        )
        update_cursor.close()
        updated += 1

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Done. Hashed {updated} password(s), skipped {skipped} already-hashed row(s).")


if __name__ == "__main__":
    migrate()
