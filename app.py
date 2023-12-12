from flask import Flask, render_template, redirect, request, url_for, jsonify
import sqlite3
import re

app = Flask(__name__)


@app.route('/create_employee', methods=['POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        if len(name) > 12 or re.search(r'\d', name):
            return "Введите корректное имя"

        if not re.match(r'^\+\d{10,15}$', phone):
            return "Введите номер через + без пробелом, попробуйте снова"

        conn = sqlite3.connect('i_shop.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO employees (name, phone) VALUES (?, ?)', (name, phone))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))


@app.route('/get_employees', methods=['GET'])
def get_all_employees():
    conn = sqlite3.connect('i_shop.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employees')
    employees_data = cursor.fetchall()

    conn.close()

    return render_template('employees_list.html', employees=employees_data)


@app.route('/update_employee', methods=['POST'])
def update_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        phone = request.form['phone']

        try:
            if not re.match(r'^[A-Za-z\s]+$', name):
                return "Ошибка: Неверный формат имени, введите корректно"

            if not re.match(r'^\+\d{10,15}$', phone):
                return "Ошибка: Неверный формат номера телефона, введите корректно"

            conn = sqlite3.connect('i_shop.db')
            cursor = conn.cursor()

            cursor.execute('UPDATE employees SET name = ?, phone = ? WHERE id = ?', (name, phone, employee_id))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print("Ошибка при обновлении данных сотрудника:", e)
            return "Ошибка при обновлении данных сотрудника"


@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']

        if not employee_id.isdigit():
            return "Ошибка: Неверный формат идентификатора сотрудника"
        try:
            conn = sqlite3.connect('i_shop.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print("Ошибка при удалении сотрудника:", e)
            return "Ошибка при удалении сотрудника"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/employees')
def manage_employees():
    return render_template('employees.html')


@app.route('/clients')
def manage_clients():
    return render_template('clients.html')


@app.route('/orders')
def manage_orders():
    return render_template('orders.html')


@app.route('/create_client', methods=['POST'])
def create_client():
    if request.method == 'POST':
        full_name = request.form['full_name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']

        if not re.match(r'^[A-Za-zА-Яа-яЁё\s]+$', full_name):
            return "Ошибка: Неверный формат имени"

        if not re.match(r'^[A-Za-zА-Яа-яЁё\s]+$', surname):
            return "Ошибка: Неверный форма фамилии "

        if not re.match(r'^\+\d{10,15}$', phone):
            return "Ошибка: Неверный формат номера телефона, введите корректно"

        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            return "Ошибка: Неверный формат адреса электронной почты, введите корректно"

        try:
            conn = sqlite3.connect('i_shop.db')
            cursor = conn.cursor()

            cursor.execute('INSERT INTO clients (full_name, surname, email, phone) VALUES (?, ?, ?, ?)', (full_name, surname, email, phone))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print("Ошибка при создании клиента:", e)
            return "Ошибка при создании клиента"


@app.route('/get_all_clients', methods=['GET'])
def get_all_clients():
    try:
        conn = sqlite3.connect('i_shop.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clients')
        clients_data = cursor.fetchall()

        conn.close()

        return render_template('clients_list.html', clients=clients_data)
    except Exception as e:
        print("Ошибка при получении списка клиентов:", e)
        return "Ошибка при получении списка клиентов"

@app.route('/delete_client', methods=['POST'])
def delete_client():
    if request.method == 'POST':
        client_id = request.form['client_id']

        if not client_id.isdigit():
            return "Ошибка: Неверный формат идентификатора клиента"
        try:
            conn = sqlite3.connect('i_shop.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print("Ошибка при удалении сотрудника:", e)
            return "Ошибка при удалении сотрудника"


def is_employee_exists(employee_id):
    conn = sqlite3.connect('i_shop.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = cursor.fetchone()

    conn.close()

    return bool(employee)

def is_client_exists(client_id):
    conn = sqlite3.connect('i_shop.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client = cursor.fetchone()

    conn.close()

    return bool(client)

def is_product_exists(product_id):
    conn = sqlite3.connect('i_shop.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    conn.close()

    return bool(product)
@app.route('/create_order', methods=['POST'])
def create_order():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        client_id = request.form['client_id']
        product_id = request.form['product_id']

        # Разделите введенные ID товаров с помощью запятой и преобразуйте в список
        product_id_list = [int(product_id.strip()) for product_id in product_id.split(',') if product_id.strip()]

        conn = sqlite3.connect('i_shop.db')
        cursor = conn.cursor()

        for product_id in product_id_list:
            cursor.execute('''
                SELECT * FROM orders
                WHERE employee_id = ? AND client_id = ? AND product_id = ?
            ''', (employee_id, client_id, product_id))

            existing_order = cursor.fetchone()

            if existing_order:
                return f"Заказ с товаром {product_id} уже существует"

            if not is_product_exists(product_id):
                return f"Товар с ID {product_id} не существует"

            cursor.execute('''
                INSERT INTO orders (employee_id, client_id, product_id)
                VALUES (?, ?, ?)
            ''', (employee_id, client_id, product_id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/delete_order', methods=['POST'])
def delete_order():
    if request.method == 'POST':
        order_id = request.form['order_id']

        if not order_id.isdigit():
            return "Ошибка: Неверный формат идентификатора заказа"
        try:
            conn = sqlite3.connect('i_shop.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
            cursor.execute('INSERT INTO shopping_cart (order_id) VALUES (?)', (order_id,))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print("Ошибка при удалении заказа:", e)
            return "Ошибка при удалении заказа"


def get_product_price_by_id(product_id):
    conn = sqlite3.connect('i_shop.db')
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
    price = cursor.fetchone()

    conn.close()

    return price[0] if price else None

@app.route('/calculate_order_cost', methods=['POST'])
def calculate_order_cost():
    data = request.json

    product_id = data.get('product_ids')

    total_order_cost = 0

    for product_id in product_id:
        price = get_product_price_by_id(product_id)
        if price:
            total_order_cost += price

    return jsonify({'order_cost': total_order_cost})

if __name__ == '__main__':
    app.run(debug=True)