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
    # order_id = db.Column(db.Integer)
    # executor_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    orders = db.relationship("Order")
    users = db.relationship('User')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    # customer_id = db.Column(db.Integer)
    # executor_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', foreign_keys=[customer_id])
    user1 = db.relationship('User', foreign_keys=[executor_id])


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
                executor_id=offer['executor_id']
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
                price=order['price']
            )
        )
        with db.session.begin():
            db.session.add_all(new_orders)


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
    try:
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
    except:
        return 'Неверные данные'


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
    new_user_dict = {}
    new_user_dict['id'] = new_user.id
    new_user_dict['first_name'] = new_user.first_name
    new_user_dict['last_name'] = new_user.last_name
    new_user_dict['age'] = new_user.age
    new_user_dict['email'] = new_user.email
    new_user_dict['role'] = new_user.role
    new_user_dict['phone'] = new_user.phone

    return 'Новый пользователь добавлен в базу!', 201


# Реализуйте обновление пользователя `user` посредством метода PUT на URL `/users/<id>`  для users.
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user_for_update = User.query.get(id)
        data_to_update = request.json
        setattr(user_for_update, 'first_name', data_to_update['first_name'])
        setattr(user_for_update, 'last_name', data_to_update['last_name'])
        setattr(user_for_update, 'age', data_to_update['age'])
        setattr(user_for_update, 'email', data_to_update['email'])
        setattr(user_for_update, 'role', data_to_update['role'])
        setattr(user_for_update, 'phone', data_to_update['phone'])

        db.session.add(user_for_update)
        db.session.commit()
        db.session.close()

        return 'Данные изменены', 200
    except Exception: 'Неверные данные ¯\_(ツ)_/¯', 404


# В Body будет приходить JSON со всеми полями для обновление заказа.
# Реализуйте удаление пользователя `user` посредством метода DELETE на URL `/users/<id>` для users.
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return 'Удалено, молодец))))', 204


# ШАГ 7
# Реализуйте создание заказа order посредством метода POST на URL /orders  для orders.
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    new_order = Order(
        id=order_data.get('id'),
        name=order_data.get('name'),
        description=order_data.get('description'),
        start_date=order_data.get('start_date'),
        end_date=order_data.get('end_date'),
        address=order_data.get('address'),
        price=order_data.get('price')
    )
    db.session.add(new_order)
    db.session.commit()
    new_order_dict = {}
    new_order_dict['id'] = new_order.id
    new_order_dict['name'] = new_order.name
    new_order_dict['description'] = new_order.description
    new_order_dict['start_date'] = new_order.start_date
    new_order_dict['end_date'] = new_order.end_date
    new_order_dict['address'] = new_order.address
    new_order_dict['price'] = new_order.price

    return 'Новый заказ добавлен в базу!', 201


# Реализуйте обновление заказа order посредством метода PUT на URL /orders/<id>  для orders.
# В Body будет приходить JSON со всеми полями для обновление заказа.
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order_for_update = Order.query.get(id)
        data_to_update = request.json
        setattr(order_for_update, 'name', data_to_update['name'])
        setattr(order_for_update, 'description', data_to_update['description'])
        setattr(order_for_update, 'start_date', data_to_update['start_date'])
        setattr(order_for_update, 'end_date', data_to_update['end_date'])
        setattr(order_for_update, 'address', data_to_update['address'])
        setattr(order_for_update, 'address', data_to_update['address'])
        setattr(order_for_update, 'price', data_to_update['price'])
        db.session.add(order_for_update)
        db.session.commit()
        db.session.close()

        return 'Данные изменены', 200
    except Exception: 'Неверные данные ¯\_(ツ)_/¯', 404


# Реализуйте удаление заказа order посредством метода DELETE на URL /orders/<id> для orders.
@app.route('/orders/<int:id>/delete')
def delete_order(id):
    order_to_delete = Order.query.get(id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return 'Ну, молодец, удалил важный заказ))))', 204


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
    new_offer_dict = {}
    new_offer_dict['id'] = new_offer.id
    new_offer_dict['offer_id'] = new_offer.ioffer_idd
    new_offer_dict['executor_id'] = new_offer.executor_id

    return 'Новый оффер добавлен в базу!', 201


# Реализуйте обновление предложения offer посредством метода PUT на URL /offers/<id> для offers.
# В Body будет приходить JSON со всеми полями для обновление предложения.
@app.route('/offers/<int:id>', methods=['PUT'])
def replace_offer(id):
    try:
        offer_to_replace = Offer.query.get(id)
        data_to_update = request.json
        setattr(offer_to_replace, 'order_id', data_to_update['order_id'])
        setattr(offer_to_replace, 'executor_id', data_to_update['executor_id'])
        db.session.add(offer_to_replace)
        db.session.commit()
        db.session.close()
        return 'Оффер добавлен', 200
    except Exception: 'Неверные данные ¯\_(ツ)_/¯', 404

# Реализуйте удаление предложения offer посредством метода DELETE на URL /offers/<id> для offers.
@app.route('/offers/<int:id>/delete')
def delete_offer(id):
    offer_to_delete = Offer.query.get(id)
    db.session.delete(offer_to_delete)
    db.session.commit()
    return 'Оффер удалён', 204


if __name__ == '__main__':
    main()
