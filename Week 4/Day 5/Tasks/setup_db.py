import sqlite3

def build_enterprise_db():
    conn = sqlite3.connect('company_data.db')
    cursor = conn.cursor()

    # Clear old tables
    cursor.executescript('''
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
    ''')

    # 1. Create relational tables
    cursor.executescript('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            company_name TEXT,
            contact_person TEXT,
            phone TEXT,
            country TEXT
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    ''')

    # 2. Populate Customers
    customers = [
        (1, 'Haidereez International', 'Fayyaz', '03145390197', 'Pakistan'),
        (2, 'Silk Route International Trading', 'Muhammad Fazil', 'N/A', 'Pakistan'),
        (3, 'Charlie Logistics', 'Alex Chen', '555-0102', 'UAE'),
        (4, 'Gilgit Weifang Import & Export', 'Wei Zhang', '555-0103', 'China')
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', customers)

    # 3. Populate Products
    products = [
        (101, 'Huawei Optical Network Terminal', 'Networking', 120.00, 450),
        (102, 'FiberHome Wi-Fi Router', 'Networking', 85.00, 200),
        (103, 'ZTE Optical Terminal', 'Networking', 110.00, 150),
        (104, 'Tenda Wireless Router', 'Networking', 45.00, 500),
        (105, 'Industrial Server Node', 'Compute', 4500.00, 10)
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)

    # 4. Populate Orders
    orders = [
        (1001, 1, '2026-08-01', 'Cleared'),
        (1002, 2, '2026-08-05', 'Pending Valuations'),
        (1003, 3, '2026-08-10', 'In Transit'),
        (1004, 4, '2026-08-15', 'Cleared')
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', orders)

    # 5. Populate Order Items
    order_items = [
        (1, 1001, 101, 50),
        (2, 1001, 104, 200),
        (3, 1002, 102, 100),
        (4, 1003, 105, 5),
        (5, 1004, 103, 75)
    ]
    cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?)', order_items)

    conn.commit()
    conn.close()
    print("Enterprise relational database created successfully!")

if __name__ == "__main__":
    build_enterprise_db()