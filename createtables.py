import sqlite3
import random
import string

with sqlite3.connect('i_shop.db') as db:
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
        surname TEXT NOT NULL,
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
        product_id INTEGER,
        order_cost INTEGER,
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

# Функция для создания случайного имени продукта

def generate_name():
    return ''.join(random.choices(string.ascii_letters, k=random.randint(5, 15)))

# Функция для создания случайной цены в заданном диапазоне
def generate_price():
    return random.randint(100, 100000)

# Функция для создания случайного веса в заданном диапазоне
def generate_weight():
    return round(random.uniform(1, 10), 2)

# Функция для создания случайного размера в заданном диапазоне
def generate_size():
    return round(random.uniform(0.1, 10), 2)

# Функция для создания случайного текстового описания
def generate_description():
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(20, 100))).encode('utf-8')


# Подключение к базе данных
conn = sqlite3.connect('i_shop.db')
cursor = conn.cursor()

# Создание 1000 записей с валидными значениями для полей таблицы
for _ in range(1000):
    name = generate_name()
    price = generate_price()
    weight = generate_weight()
    size = generate_size()
    description = generate_description()

    # Вставка данных в таблицу products
    cursor.execute('''
        INSERT INTO products (name, price, weight, size, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, price, weight, size, description))

conn.commit()
conn.close()