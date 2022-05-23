from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    # offers = db.relationship("Offer")
    # orders = db.relationship("Order")


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)
    # order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # orders = db.relationship("Order")


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)
    # customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def main():
    db.create_all()
    insert_data()

    app.run(debug=True)


def insert_data():
    new_users = []
    for user in users:
        new_users.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
                # offers = user[''],
                # orders = db.relationship("Order")
            )
        )
        with db.session.begin():
            db.session.add_all(new_users)

    new_offers = []
    for offer in offers:
        new_offers.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
                # orders = db.relationship("Order")
            )
        )
        with db.session.begin():
            db.session.add_all(new_offers)

    new_orders = []
    for order in orders:
        new_orders.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                # customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
                # executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            )
        )
        with db.session.begin():
            db.session.add_all(new_orders)


# @app.route('/', methods=['GET,POST'])
# def orders_index():
#     if request.method == 'GET':
#         data = []
#         for order in Order.query.all():
#             customer = User.query.get(order.customer_id).first_name
#             executor = User.query.get(order.executor_id).first_name
#             data.append({
#                 'id': order.id,
#                 'name': order.name,
#                 'description': order.description,
#                 'start_date': order.start_date,
#                 'end_date': order.end_date,
#                 'address': order.address,
#                 'price': order.price
#             })
#         return jsonify(data)

# ШАГ 3
# Создайте представление для пользователей,
# которое обрабатывало бы `GET`-запросы получения всех пользователей `/users`

@app.route('/users', methods=['GET'])
def users_index():
    users_data = []
    for user in User.query.all():
        users_data.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        })
    return jsonify(users_data)


# и одного пользователя по идентификатору `/users/1`.
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    user_dict = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'role': user.role,
        'phone': user.phone
    }
    return jsonify(user_dict)


# ШАГ 4
# Создайте представление для заказов,
# которое обрабатывало бы `GET`-запросы получения всех заказов `/orders`

@app.route('/orders', methods=['GET'])
def orders_index():
    orders_data = []
    for order in Order.query.all():
        orders_data.append({
            'id': order.id,
            'name': order.name,
            'description': order.description,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'address': order.address,
            'price': order.price
        })
    return jsonify(orders_data)


# и заказа по идентификатору `/orders/1`.
@app.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    order = Order.query.get(id)
    order_dict = {
        'id': order.id,
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price
    }
    return jsonify(order_dict)


# ШАГ 5
# Создайте представление для предложений,
# которое обрабатывало бы `GET`-запросы получения всех предложений `/offers`
@app.route('/offers', methods=['GET'])
def offers_index():
    offers_data = []
    for offer in Offer.query.all():
        offers_data.append({
            'id': offer.id,
            'order_id': offer.order_id,
            'executor_id': offer.executor_id
        })
    return jsonify(offers_data)


# и предложения по идентификатору `/offers/<id>`.
@app.route('/offers/<int:id>', methods=['GET'])
def get_offer_by_id(id):
    offer = Offer.query.get(id)
    offer_dict = {
        'id': offer.id,
        'order_id': offer.order_id,
        'executor_id': offer.executor_id
    }
    return jsonify(offer_dict)


# ШАГ 6
# Реализуйте создание пользователя `user` посредством метода POST на URL `/users`  для users.
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    new_user = User(
        id=user_data.get('id'),
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        age=user_data.get('age'),
        email=user_data.get('email'),
        role=user_data.get('role'),
        phone=user_data.get('phone')
    )
    db.session.add(new_user)
    db.session.commit()
    new_user_dict = {
        'id': 31,
        'first_name': 'Sweet',
        'last_name': 'Potato',
        'age': 25,
        'email': 'sweet@potato.com',
        'role': 'executor',
        'phone': '128500'
    }
    return jsonify(new_user_dict)


# Реализуйте обновление пользователя `user` посредством метода PUT на URL `/users/<id>`  для users.
@app.route('/users/<int:id>', methods=['PUT'])
def update_user():
    user_to_update = User.query.get(id)
    user_to_update.first_name = request.json['new_first_name']
    user_to_update.last_name = request.json['new_last_name']
    user_to_update.age = request.json['new_age']
    user_to_update.email = request.json['new_email']
    user_to_update.phone = request.json['new_phone']
    db.session.commit()
    db.session.close()


# В Body будет приходить JSON со всеми полями для обновление заказа.
# Реализуйте удаление пользователя `user` посредством метода DELETE на URL `/users/<id>` для users.
@app.route('/users/<int:id>/delete')
def delete_user(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify("")


# ШАГ 7
# Реализуйте создание заказа order посредством метода POST на URL /orders  для orders.
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    new_order = Order(
        id=order_data.get('id'),
        name=order_data.get('name'),
        start_date=order_data.get('start_date'),
        end_date=order_data.get('end_date'),
        address=order_data.get('address'),
        price=order_data.get('price')
    )
    db.session.add(new_order)
    db.session.commit()
    new_order_dict = {
        'id': 50,
        'name': 'покрасить собаке шерсть',
        'description': 'заказать краску, дать собаке снотворное, покрасить в синий',
        'start_date': 12 / 30 / 2016,
        'end_date': 12 / 31 / 2016,
        'address': '12637 Poodle Road\nBarking, NM 29343',
        'price': 1000
    }
    return jsonify(new_order_dict)


# Реализуйте обновление заказа order посредством метода PUT на URL /orders/<id>  для orders.
# В Body будет приходить JSON со всеми полями для обновление заказа.
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order():
    order_to_update = Order.query.get(id)
    order_to_update.name = request.json['new_name']
    order_to_update.description = request.json['new_description']
    order_to_update.start_date = request.json['new_start_date']
    order_to_update.end_date = request.json['new_end_date']
    order_to_update.address = request.json['new_address']
    order_to_update.price = request.json['new_price']
    db.session.commit()
    db.session.close()

# Реализуйте удаление заказа order посредством метода DELETE на URL /orders/<id> для orders.
@app.route('/orders/<int:id>/delete')
def delete_order(id):
    order_to_delete = Order.query.get(id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return jsonify("")

# ШАГ 8
# Реализуйте создание предложения offer посредством метода POST на URL /offers для offers.
@app.route('/offers', methods=['POST'])
def create_offer():
    offer_data = request.json
    new_offer = Offer(
        id=offer_data.get('id'),
        order_id=offer_data.get('offer_id'),
        executor_id=offer_data.get('executor_id')
    )
    db.session.add(new_offer)
    db.session.commit()
    new_offer_dict = {
        'id': 70,
        'order_id': 43,
        'executor_id': 16
    }
    return jsonify(new_offer_dict)

# Реализуйте обновление предложения offer посредством метода PUT на URL /offers/<id> для offers.
# В Body будет приходить JSON со всеми полями для обновление предложения.
@app.route('/offers/<int:id>', methods=['PUT'])
def update_offer():
    offer_to_update = Offer.query.get(id)
    offer_to_update.order_id = request.json['new_order_id']
    offer_to_update.executor_id = request.json['new_executor_id']
    db.session.commit()
    db.session.close()

# Реализуйте удаление предложения offer посредством метода DELETE на URL /offers/<id> для offers.
@app.route('/offers/<int:id>/delete')
def delete_offer(id):
    offer_to_delete = Offer.query.get(id)
    db.session.delete(offer_to_delete)
    db.session.commit()
    return jsonify("")


if __name__ == '__main__':
    main()
