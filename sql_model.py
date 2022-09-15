from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from discount_controller import *

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://ericbanzuzi:mysql00eb@localhost/dbproject'
db = SQLAlchemy(app)

margin = 1.4
vat = 1.09
fmt = '%Y-%m-%d %H:%M:%S'  # for datetime calculations


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    # relationships, many to one
    address = db.relationship('Address', back_populates='customer')
    order = db.relationship('Orders', back_populates='customer')

    def __repr__(self):
        return f'Customer({self.firstname}, {self.lastname}, {self.phone_number}, {self.address})'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(80), nullable=False)
    house_number = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)

    customer = db.relationship('Customer', order_by=Customer.id, back_populates="address")

    def __repr__(self):
        return f'Address({self.street}, {self.house_number}, {self.city}, {self.postcode})'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    datetime = db.Column(db.DateTime, nullable=False)
    discount_code = db.Column(db.Boolean, nullable=False)

    # relationships
    customer = db.relationship('Customer', back_populates='order', uselist=False) # many to one
    delivery = db.relationship('DeliveryPerson', secondary='delivery', back_populates='delivery', uselist=False) # one to one

    def __repr__(self):
        return f'Orders({self.customer_id}, {self.datetime}, {self.discount_code})'


class Orderline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))
    desert_id = db.Column(db.Integer, db.ForeignKey('desert.id'))
    quantity = db.Column(db.Integer, nullable=False)

    # relationships, many to many
    order = db.relationship('Orders')
    pizza = db.relationship('Pizza')
    drink = db.relationship('Drink')
    desert = db.relationship('Desert')

    def __repr__(self):
        return f'Orderline({self.order_id}, {self.pizza_id}, {self.drink_id}, {self.desert_id}, {self.quantity})'


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # relationships
    toppings = db.relationship('Topping', secondary='pizza_toppings', back_populates='pizza')

    def __repr__(self):
        return f'Pizza({self.name})'


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(6, 2), nullable=False)

    def __repr__(self):
        return f'Drink({self.name}, {self.price})'


class Desert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(6, 2), nullable=False)

    def __repr__(self):
        return f'Desert({self.name}, {self.price})'


class Topping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(6, 2), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)

    # relationships
    pizza = db.relationship('Pizza', secondary='pizza_toppings', back_populates='toppings')

    def __repr__(self):
        return f'Topping({self.name}, {self.price}, {self.vegetarian})'


class PizzaToppings(db.Model):
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), primary_key=True)
    topping_id = db.Column(db.Integer, db.ForeignKey('topping.id'), primary_key=True)

    def __repr__(self):
        return f'Pizza_toppings({self.pizza_id}, {self.topping_id})'


class DeliveryPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area_code = db.Column(db.String(10), nullable=False)

    # relationships, many to one
    delivery = db.relationship('Orders', secondary='delivery', back_populates='delivery')

    def __repr__(self):
        return f'Delivery_person({self.area_code})'


class Delivery(db.Model):
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('delivery_person.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    estimated_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Delivery({self.delivery_person_id}, {self.order_id}, {self.estimated_time})'


# run only once to initialize the menu data
def create_menu():
    mozzarella = Topping(name='mozzarella', price=1.59, vegetarian=True)
    tomato_sauce = Topping(name='tomato sauce', price=0.99, vegetarian=True)
    oregano = Topping(name='oregano', price=0.49, vegetarian=True)
    ham = Topping(name='ham', price=2.49, vegetarian=False)
    pineapple = Topping(name='pineapple', price=1.20, vegetarian=True)
    mushroom = Topping(name='mushroom', price=1.00, vegetarian=True)
    onion = Topping(name='onion', price=0.39, vegetarian=True)
    pepper = Topping(name='pepper', price=1.20, vegetarian=True)
    tomato = Topping(name='tomato', price=0.49, vegetarian=True)
    spicy_salami = Topping(name="spicy salami", price=2.99, vegetarian=False)
    pepperoni = Topping(name='pepperoni', price=2.49, vegetarian=False)
    egg = Topping(name='egg', price=1.49, vegetarian=True)
    chicken = Topping(name='chicken', price=2.49, vegetarian=False)
    eggplant = Topping(name='eggplant', price=1.49, vegetarian=True)

    pizza = Pizza(name='Margherita')
    pizza.toppings = [
        tomato_sauce, mozzarella, oregano, Topping(name='garlic oil', price=0.49, vegetarian=True)
    ]
    pizza2 = Pizza(name='Hawaii')
    pizza2.toppings = [
        tomato_sauce, mozzarella,  ham, pineapple
    ]
    pizza3 = Pizza(name='Veggie')
    pizza3.toppings = [
        tomato_sauce, mozzarella, onion, tomato, mushroom, pepper
    ]
    pizza4 = Pizza(name='Forest')
    pizza4.toppings = [
        tomato_sauce, mozzarella, mushroom, ham
    ]
    pizza5 = Pizza(name='Diavolo')
    pizza5.toppings = [
        tomato_sauce, mozzarella, spicy_salami, onion, pepper
    ]
    pizza6 = Pizza(name='Pepperoni')
    pizza6.toppings = [
        tomato_sauce, mozzarella, pepperoni
    ]
    pizza7 = Pizza(name='Peppel Pizza')
    pizza7.toppings = [
        tomato_sauce, mozzarella, pepperoni, pepper, chicken
    ]
    pizza8 = Pizza(name='Romano')
    pizza8.toppings = [
        tomato_sauce, mozzarella, oregano, spicy_salami, egg, tomato
    ]
    pizza9 = Pizza(name='Veggie Deluxe')
    pizza9.toppings = [
        tomato_sauce, mozzarella, onion, tomato, mushroom, pepper, oregano, eggplant
    ]
    pizza10 = Pizza(name='Meatlovers')
    pizza10.toppings = [
        tomato_sauce, pepperoni, spicy_salami, ham, chicken, onion
    ]

    # drinks
    coke = Drink(name='Coca-Cola', price=1.99)
    fanta = Drink(name='Fanta', price=1.99)
    sprite = Drink(name='Sprite', price=1.99)
    iced_tea =Drink(name='Iced-Tea', price = 1.99)

    # deserts
    cheese_cake = Desert(name='Cheese cake', price=3.50)
    ice_cream = Desert(name='Ice cream', price=2.50)

    db.session.add_all([
        pizza, pizza2, pizza3, pizza4, pizza5, pizza6, pizza7, pizza8, pizza9, pizza10,
        coke, fanta, sprite, iced_tea, cheese_cake, ice_cream
    ])
    db.session.commit()


# run only once to initialize the delivery persons
def create_delivery_persons():
    db.session.add_all([
        DeliveryPerson(area_code='60'),
        DeliveryPerson(area_code='60'),
        DeliveryPerson(area_code='61'),
        DeliveryPerson(area_code='61'),
        DeliveryPerson(area_code='62'),
        DeliveryPerson(area_code='62'),
        DeliveryPerson(area_code='63'),
        DeliveryPerson(area_code='63'),
        DeliveryPerson(area_code='64'),
        DeliveryPerson(area_code='64')
    ])
    db.session.commit()


def save_new_customer(firstname, lastname, phone_number, street, house_number, city, postcode):
    new_customer = Customer(firstname=firstname, lastname=lastname, phone_number=phone_number)

    address = find_single_address(street=street, house_number=house_number, city=city, postcode=postcode)
    if address is None:
        address = Address(street=street, house_number=house_number, city=city, postcode=postcode)

    address.customer = address.customer + [new_customer]
    db.session.add(new_customer)
    db.session.commit()
    return new_customer


def save_new_order(customer_id, time, code):

    if check_discount(code):
        new_order = Orders(customer_id=customer_id, datetime=time, discount_code=True)
    else:
        new_order = Orders(customer_id=customer_id, datetime=time, discount_code=False)

    db.session.add(new_order)
    db.session.commit()
    return new_order


def save_new_orderline(order_id, item_type, item_id, quantity):

    if item_type == 'Pizza':
        new_orderline = Orderline(order_id=order_id, pizza_id=item_id, quantity=quantity)
    elif item_type == 'Drink':
        new_orderline = Orderline(order_id=order_id, drink_id=item_id, quantity=quantity)
    else:
        new_orderline = Orderline(order_id=order_id, desert_id=item_id, quantity=quantity)

    db.session.add(new_orderline)
    db.session.commit()
    return new_orderline


def save_new_delivery(delivery_person_id, order_id, estimated_time):
    new_delivery = Delivery(delivery_person_id=delivery_person_id, order_id=order_id, estimated_time=estimated_time)
    db.session.add(new_delivery)
    db.session.commit()
    return new_delivery


def find_single_address(**kwargs):
    return Address.query.filter_by(**kwargs).first()


def find_single_customer(**kwargs):
    return Customer.query.filter_by(**kwargs).first()


def find_single_order(**kwargs):
    return Orders.query.filter_by(**kwargs).first()


def find_single_delivery(**kwargs):
    return Delivery.query.filter_by(**kwargs).first()


def find_single_drink(**kwargs):
    return Drink.query.filter_by(**kwargs).first()


def find_single_desert(**kwargs):
    return Desert.query.filter_by(**kwargs).first()


def delete_single_delivery(**kwargs):
    delivery = find_single_delivery(**kwargs)  # maybe give back the discount code, let's see
    db.session.delete(delivery)
    db.session.commit()


def save_available_delivery(order, postcode, time):
    area = postcode[:2]

    person_time = []
    times = []

    for person in DeliveryPerson.query.filter_by(area_code=area).all():
        deliveries = [delivery for delivery in Delivery.query.filter_by(delivery_person_id=person.id).all()]
        # person has no deliveries
        if len(deliveries) == 0:
            return save_new_delivery(delivery_person_id=person.id, order_id=order.id,
                                     estimated_time=(time + timedelta(minutes=15)))
        else:
            # the person can still take the order in same delivery
            d1 = datetime.strptime(str(deliveries[-1].estimated_time), fmt)
            d2 = datetime.strptime(str(time), fmt)
            diff = (d1 - timedelta(minutes=10)) - d2

            if diff.days == 0 and (diff.seconds/60) <= 5:
                return save_new_delivery(delivery_person_id=person.id, order_id=order.id,
                                         estimated_time=d1)
            # the person has come back
            diff = d2 - d1
            if diff.days == 0 and diff.seconds / 60 >= 20:
                return save_new_delivery(delivery_person_id=person.id, order_id=order.id,
                                         estimated_time=(d2 + timedelta(minutes=15)))
        person_time.append((person, d1))
        times.append(diff)

    i = times.index(max(times))
    got_back = person_time[i][1] + timedelta(minutes=20)
    diff = got_back - time
    minutes_add = int(diff.seconds/60)
    return save_new_delivery(delivery_person_id=person_time[i][0].id, order_id=order.id, estimated_time=(d2+timedelta(minutes=15+minutes_add)))


def get_pizza_info(pizza_id):
    info = ('', 0)
    for name, total_price in db.session.query(Pizza.name, func.sum(Topping.price * margin)).select_from(Pizza).join(PizzaToppings).\
            join(Topping).group_by(Pizza.id).filter(Pizza.id==pizza_id).all():
        price = round(total_price * vat, 2)
        pizza = name
        info = (pizza, price)
    return info


def get_pizza_count(customer_id):
    customer = find_single_customer(id=customer_id)
    count = 0
    for order in Orders.query.filter_by(customer_id=customer.id).all():
        for orderline in Orderline.query.filter_by(order_id=order.id).all():
            if order.delivery is not None and orderline.pizza_id is not None:
                count = count + orderline.quantity
    return count


def show_menu():
    print()
    print('MENU:')
    for pizza, total_price, vegetarian in db.session.query(Pizza, func.sum(Topping.price * margin), func.count(db.case([(Topping.vegetarian, 1)]))).select_from(Pizza).join(PizzaToppings).\
            join(Topping).group_by(Pizza.id).order_by(Pizza.id).all():
        if vegetarian == len(pizza.toppings):
            print(str(pizza.id) + '. ' + pizza.name + ' (V) ' + str(round(total_price * vat, 2)))
        else:
            print(str(pizza.id) + '. ' + pizza.name + '  ' + str(round(total_price * vat, 2)))
        print([topping.name for topping in pizza.toppings])

    print()
    print('DRINKS:')
    for drink in db.session.query(Drink).order_by(Drink.id).all():
        print(str(drink.id) + '. ' + drink.name + '  ' + str(drink.price))

    print()
    print('DESERTS:')
    for desert in db.session.query(Desert).order_by(Desert.id).all():
        print(str(desert.id) + '. ' + desert.name + '  ' + str(desert.price))
    print()


def show_order():
    db.session.commit()  # put database up to date
    print()
    print('ORDER:')
    order = Orders.query.order_by(Orders.id.desc()).first()
    delivery = find_single_delivery(order_id=order.id)

    pizzas = []
    drinks = []
    deserts = []
    total = 0

    if order.discount_code:
        discount = 0.9
    else:
        discount = 1

    for orderline in Orderline.query.filter(Orderline.order_id == order.id).all():
        if orderline.pizza_id is not None:
            info = get_pizza_info(orderline.pizza_id)
            pizzas.append((info[0], info[1], orderline.quantity))
            total = total + round(info[1]*orderline.quantity*discount, 2)
        elif orderline.drink_id is not None:
            drink = find_single_drink(id=orderline.drink_id)
            drinks.append((drink.name, drink.price, orderline.quantity))
            total = total + round(float(drink.price)*orderline.quantity*discount, 2)
        elif orderline.desert_id is not None:
            desert = find_single_desert(id=orderline.desert_id)
            deserts.append((desert.name, desert.price, orderline.quantity))
            total = total + round(float(desert.price)*orderline.quantity*discount, 2)

    print('Your order (id): '+str(order.id)+' is estimated to arrive at: '+str(delivery.estimated_time))

    print('Order summary:')
    for i in range(len(pizzas)):
        print(' - '+str(pizzas[i][0])+' x '+str(pizzas[i][2])+'  cost:  '+str(round(pizzas[i][1]*pizzas[i][2]*discount, 2)))

    for i in range(len(drinks)):
        print(' - '+str(drinks[i][0])+' x '+str(drinks[i][2])+'  cost:  '+str(round(drinks[i][1]*drinks[i][2]*discount, 2)))

    for i in range(len(deserts)):
        print(' - '+str(deserts[i][0])+' x '+str(deserts[i][2])+'  cost:  '+str(round(deserts[i][1]*deserts[i][2]*discount, 2)))

    print('Total price: '+str(total))

    count = get_pizza_count(order.customer_id)
    if count != 0 and count % 10 == 0:
        print('Use this code for next order to get discount: ' + new_discount_code())


db.create_all()
