from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import psycopg2 # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")


app = Flask(__name__)
app.secret_key = 'your_secret_key'
products = [
    {'id': 1, 'name': 'Корм для собак', 'price': 600, 'disc': "Сбалансированное питание для здоровья и энергии вашего питомца."},
    {'id': 2, 'name': 'Корм для кошек', 'price': 600, 'disc': "Вкусные гранулы с витаминами для активной жизни кошки."},
    {'id': 3, 'name': 'Корм для собак DELUXE', 'price': 1200, 'disc': "Премиум-рацион с мясом и овощами для идеальной формы."},
    {'id': 4, 'name': 'Корм для кошек DELUXE', 'price': 1337, 'disc': " Высококачественные ингредиенты для блестящей шерсти и здоровья."},
    {'id': 5, 'name': 'Игрушка для питомца "мячик"', 'price': 160, 'disc': "Прочная и экологичная игрушка для активного отдыха вашего питомца."},
    {'id': 6, 'name': 'Домик для кошки', 'price': 900, 'disc': "Комфотное жилье для кошек из lower middle class, хорошая шумоизоляция, качественное отопление."},

    {'id': 7, 'name': 'когтеточка "столбик" 54см', 'price': 540, 'disc': "Бежевый столбик для когтей вашей кошки."},
    {'id': 8, 'name': 'Светодиодный ошейник', 'price': 750, 'disc': "Эстетичный отблеск поможет вашей собаке не потеряться в темноте."},
    {'id': 9, 'name': 'Товар 9', 'price': 45, 'disc': ""},
    {'id': 10, 'name': 'Товар 10', 'price': 4500, 'disc': ""}

]

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    return "Товар не найден", 404
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].remove(product_id)
    session.modified = True
    print(session['cart'])
    if 'username' in session:
        username = session['username']
        try:
                connection = psycopg2.connect(
                    user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
                )
                cursor = connection.cursor()

                cart_items = []
                if 'cart' in session:
                    for product_id in session['cart']:
                        product = next((p for p in products if p['id'] == product_id), None)
                        if product:
                            cart_items.append(product)
                
                    text_cart_items = ([int(i['id']) for i in cart_items])
                    text_cart_items = str(text_cart_items)[1:-1]
                    print(999, cart_items)
                    print(text_cart_items)
    
                    cursor.execute(
                        "UPDATE users SET cart = %s WHERE username = %s",
                        (text_cart_items,username)
                    )

                connection.commit()
                cursor.close()
                connection.close()

        except Exception as e:
                print(e)
                return redirect(url_for('cart'))
    return redirect(url_for('cart'))

@app.route('/add_to_cart_from_card/<int:product_id>')
def add_to_cart_from_card(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    product = next((p for p in products if p['id'] == product_id), None)
    print(session['cart'])
    if 'username' in session:
        username = session['username']
        try:
                connection = psycopg2.connect(
                    user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
                )
                cursor = connection.cursor()

                cart_items = []
                if 'cart' in session:
                    for product_id in session['cart']:
                        product = next((p for p in products if p['id'] == product_id), None)
                        if product:
                            cart_items.append(product)
                
                    text_cart_items = ([int(i['id']) for i in cart_items])
                    text_cart_items = str(text_cart_items)[1:-1]
                    print(999, cart_items)  
                    print(text_cart_items)
    
                    cursor.execute(
                        "UPDATE users SET cart = %s WHERE username = %s",
                        (text_cart_items,username)
                    )

                connection.commit()
                cursor.close()
                connection.close()

        except Exception as e:
                print(e)
                return render_template('product.html', product=product)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    print(session['cart'])
    if 'username' in session:
        username = session['username']
        try:
                connection = psycopg2.connect(
                    user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
                )
                cursor = connection.cursor()

                cart_items = []
                if 'cart' in session:
                    for product_id in session['cart']:
                        product = next((p for p in products if p['id'] == product_id), None)
                        if product:
                            cart_items.append(product)
                
                    text_cart_items = ([int(i['id']) for i in cart_items])
                    text_cart_items = str(text_cart_items)[1:-1]
                    print(999, cart_items)  
                    print(text_cart_items)
    
                    cursor.execute(
                        "UPDATE users SET cart = %s WHERE username = %s",
                        (text_cart_items,username)
                    )

                connection.commit()
                cursor.close()
                connection.close()

        except Exception as e:
                print(e)
                return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    if 'username' not in session:
        cart_items = []
        order_confirmed = session.pop('order_confirmed', False)
        if 'cart' in session:
            for product_id in session['cart']:
                product = next((p for p in products if p['id'] == product_id), None)
                if product:
                    cart_items.append(product)
        if len(cart_items) < 1:
            flash('Здесь появятся Ваши покупки!')
        return render_template('cart.html', products=cart_items, order_confirmed=order_confirmed)
    else:
        username = session['username']
        cart_items = []
        order_confirmed = session.pop('order_confirmed', False)
        if 'cart' in session:
            for product_id in session['cart']:
                product = next((p for p in products if p['id'] == product_id), None)
                if product:
                    cart_items.append(product)
        if len(cart_items) < 1:
            flash('Здесь появятся Ваши покупки!')
        return render_template('cart.html', products=cart_items, order_confirmed=order_confirmed)
      

    

@app.route('/checkout')
def checkout():
    if 'cart' in session and len(session['cart']) > 0:
        if 'username' in session:
            session.pop('cart')
            session['order_confirmed'] = True
            username = session['username']
            try:
                        connection = psycopg2.connect(
                            user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
                        )
                        cursor = connection.cursor()
            
                        cursor.execute(
                                "UPDATE users SET cart = %s WHERE username = %s",
                                ('',username)
                            )
                        connection.commit()
                        cursor.close()
                        connection.close()
                        return redirect(url_for('cart'))

            except Exception as e:
                        print(e)
                        return redirect(url_for('cart'))
        else:
            flash('Зарегестрируйтесь, чтобы оформить заказ!', 'error')
            return redirect(url_for('cart'))
    else:
        flash('Оформить заказ пока нельзя! Добавьте хотя бы один товар в корзину!', 'error')
        return redirect(url_for('cart'))


@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DBNAME
            )
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result and result[0] == password:
                cart_items = []
                if 'cart' in session:
                    for product_id in session['cart']:
                        product = next((p for p in products if p['id'] == product_id), None)
                        if product:
                            cart_items.append(product)

                cursor.execute("SELECT cart FROM users WHERE username = %s", (username,))
                res = cursor.fetchone()[0]

                if res:
                    res = list(map(int, res.split(',')))
                else:
                    res = []

                text_cart_items = ([int(i['id']) for i in cart_items]) + res
                text_cart_items = str(text_cart_items)[1:-1]

                session['cart'] = ([int(i['id']) for i in cart_items]) + res

                text_cart_items = ([int(i['id']) for i in cart_items]) + res
                text_cart_items = str(text_cart_items)[1:-1]
                print(2, cart_items)  
                print(text_cart_items)

                session['cart'] = ([int(i['id']) for i in cart_items]) + res
                print(session['cart'])
                cursor.execute(
                    "UPDATE users SET cart = %s WHERE username = %s",
                    (text_cart_items,username)
                )

                # cursor.execute(
                #     "UPDATE users SET cart = %s WHERE username = %s",
                #     ('',username)
                # )

                connection.commit()

                session['username'] = username
                connection.close()
                return redirect(url_for('cabinet'))
            else:
                flash('Неверное имя или пароль!', 'error')
                connection.close()
                return redirect(url_for('login'))

        except Exception as e:
            flash(f"Ошибка входа: {e}", 'error')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        if 'cart' in session:
            session.pop('cart')
        return redirect(url_for('register'))
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if len(password) < 8 or len(password) > 64:
                flash('Пароль должен содержать от 8 до 64 знаков!', 'error')
                return redirect(url_for('register'))

            try:
                connection = psycopg2.connect(
                    user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
                )
                cursor = connection.cursor()

                cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    flash('Пользователь с таким именем уже существует!', 'error')
                    cursor.close()
                    connection.close()
                    return redirect(url_for('register'))

                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, password)
                )

                cart_items = []
                if 'cart' in session:
                    for product_id in session['cart']:
                        product = next((p for p in products if p['id'] == product_id), None)
                        if product:
                            cart_items.append(product)
                
                    text_cart_items = ([int(i['id']) for i in cart_items])
                    text_cart_items = str(text_cart_items)[1:-1]
                    print(2, cart_items)  
                    print(text_cart_items)
    
                    cursor.execute(
                        "UPDATE users SET cart = %s WHERE username = %s",
                        (text_cart_items,username)
                    )

                    # cursor.execute(
                    #     "UPDATE users SET cart = %s WHERE username = %s",
                    #     ('',username)
                    # )
                connection.commit()
                cursor.close()
                connection.close()

                session['username'] = username
                return redirect(url_for('cabinet'))

            except Exception as e:
                flash(f'Ошибка регистрации: {e}', 'error')
                return redirect(url_for('register'))

        return render_template('register.html')
    else:
        return redirect(url_for('cabinet'))



@app.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        cursor = connection.cursor()
        cursor.execute("SELECT email, phone, address FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        user_info = {
            'email': result[0] if result else '',
            'phone': result[1] if result else '',
            'address': result[2] if result else ''
        }

        return render_template('cabinet.html', username=username, user_info=user_info)

    except Exception as e:
        flash(f"Ошибка загрузки данных профиля: {e}", 'error')
        return redirect(url_for('index'))



@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET email = %s, phone = %s, address = %s WHERE username = %s",
            (email, phone, address, username)
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('cabinet'))

    except Exception as e:
        flash(f"Ошибка обновления профиля: {e}", 'error')
        return redirect(url_for('cabinet'))



if __name__ == '__main__':
    app.run(debug=True)
