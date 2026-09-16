import sqlite3

DATABASE = "foodie.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            pincode TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            items TEXT NOT NULL,
            subtotal REAL NOT NULL,
            delivery REAL NOT NULL,
            total REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()