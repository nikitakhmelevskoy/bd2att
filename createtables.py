import sqlite3

with sqlite3.connect('internet_shop.db') as db:
    cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        weight INTEGER,
        size INTEGER,
        description TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        client_id INTEGER,
        order_date DATE,
        delivery_cost INTEGER,
        order_status BOOLEAN,
        product_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees (id),
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS shopping_cart (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    )
''')
