from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)


@app.route('/create_employee', methods=['POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        conn = sqlite3.connect('internet_shop.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO employees (name, phone) VALUES (?, ?)', (name, phone))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))


@app.route('/get_employees', methods=['GET'])
def get_all_employees():
    conn = sqlite3.connect('internet_shop.db')
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
            conn = sqlite3.connect('internet_shop.db')
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

        try:
            conn = sqlite3.connect('internet_shop.db')
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
        email = request.form['email']
        phone = request.form['phone']

        try:
            conn = sqlite3.connect('internet_shop.db')
            cursor = conn.cursor()

            cursor.execute('INSERT INTO clients (full_name, email, phone) VALUES (?, ?, ?)', (full_name, email, phone))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))  # Предполагается, что 'index' - это ваша главная страница
        except Exception as e:
            print("Ошибка при создании клиента:", e)
            return "Ошибка при создании клиента"


@app.route('/get_all_clients', methods=['GET'])
def get_all_clients():
    try:
        conn = sqlite3.connect('internet_shop.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clients')
        clients_data = cursor.fetchall()

        conn.close()

        return render_template('clients_list.html', clients=clients_data)
    except Exception as e:
        print("Ошибка при получении списка клиентов:", e)
        return "Ошибка при получении списка клиентов"


@app.route('/get_all_orders', methods=['GET'])
def get_all_orders():
    try:
        conn = sqlite3.connect('internet_shop.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM orders')
        orders_data = cursor.fetchall()

        conn.close()

        return render_template('orders_list.html', orders=orders_data)
    except Exception as e:
        print("Ошибка при получении списка клиентов:", e)
        return "Ошибка при получении списка клиентов"


if __name__ == '__main__':
    app.run(debug=True)
