import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    cid = Column(Integer, primary_key=True)
    cname = Column(String)

    def __repr__(self):
        return f"Customer(cid={self.cid}, cname='{self.cname}')"


class Order(Base):
    __tablename__ = 'order1'

    oid = Column(Integer, primary_key=True)
    oDate = Column(DateTime, default=datetime.datetime.utcnow)
    cid = Column(Integer, ForeignKey('customer.cid', ondelete='CASCADE'))
    customer = relationship('Customer', backref='order1')

    def __repr__(self):
        return f"Order(oid={self.oid}, oDate='{self.oDate}', cid={self.cid})"


class Product(Base):
    __tablename__ = 'product'

    pid = Column(Integer, primary_key=True)
    pname = Column(String)
    price = Column(Integer)

    def __repr__(self):
        return f"Product(pid={self.pid}, pname='{self.pname}', price={self.price})"


class OrderItem(Base):
    __tablename__ = 'orderitem'

    iid = Column(Integer, primary_key=True)
    oid = Column(Integer, ForeignKey('order1.oid', ondelete='CASCADE'))
    order = relationship('Order', backref='order1')
    qty = Column(Integer)
    pid = Column(Integer, ForeignKey('product.pid', ondelete='CASCADE'))
    product = relationship('Product', backref='product')

    def __repr__(self):
        return f"OrderItem(iid={self.iid}, oid={self.oid}, qty={self.qty}, pid={self.pid})"


Base.metadata.create_all(engine)

session.add_all([
    Customer(cname='cust1'),
    Customer(cname='cust2')
])

session.add_all([
    Product(pname='p1', price=1000),
    Product(pname='p2', price=2000),
    Product(pname='p3', price=3000)
])

session.add_all([
    Order(cid=session.query(Customer).filter(Customer.cid == 1).first().cid),
    Order(cid=session.query(Customer).filter(Customer.cid == 2).first().cid),
    Order(cid=session.query(Customer).filter(Customer.cid == 1).first().cid)
])

session.add_all([
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 1).first().oid,
        qty=5,
        pid=session.query(Product).filter(Product.pid == 1).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 1).first().oid,
        qty=3,
        pid=session.query(Product).filter(Product.pid == 2).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 3).first().oid,
        qty=2,
        pid=session.query(Product).filter(Product.pid == 1).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 2).first().oid,
        qty=1,
        pid=session.query(Product).filter(Product.pid == 2).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 2).first().oid,
        qty=3,
        pid=session.query(Product).filter(Product.pid == 3).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 3).first().oid,
        qty=5,
        pid=session.query(Product).filter(Product.pid == 1).first().pid
    ),
    OrderItem(
        oid=session.query(Order).filter(Order.oid == 2).first().oid,
        qty=7,
        pid=session.query(Product).filter(Product.pid == 2).first().pid
    ),
])

session.commit()


def make_new_order():
    customer_name = input('\nEnter Your name: ')
    this_customer = session.query(Customer).filter(Customer.cname == customer_name).first()
    if not this_customer:
        print(f'{customer_name} customer does not exist.')
        print(f'The {customer_name} created...')
        session.add(Customer(cname=customer_name))
        session.commit()
        this_customer = session.query(Customer).filter(Customer.cname == customer_name).first()
    else:
        print(f'Continue with the {customer_name}...')

    specified_products = []
    while True:
        all_products = session.query(Product).all()
        print('\nAll Products are: ')
        for product in all_products:
            print(f'id: {product.pid}\tName: {product.pname}\tPrice: {product.price}')
        product_id = input('Enter the id of the product: ')
        if not product_id.isdigit():
            print('Product id is wrong.')
            continue
        specified_product = session.query(Product).filter(Product.pid == int(product_id)).first()
        if not specified_product:
            print('Product id is wrong.')
            continue
        count_of_product = input('Enter the count of product: ')
        if not count_of_product.isdigit():
            print('Count is wrong.')
            continue
        specified_product_with_count = {
            'product': specified_product,
            'count': int(count_of_product)
        }
        specified_products.append(specified_product_with_count)
        print(specified_products, '\n')
        stop_command = input('If the process is finished enter N... ')
        if stop_command == 'N':
            break

    session.add(Order(cid=this_customer.cid))
    session.commit()
    this_order = session.query(Order).filter(Customer.cid == this_customer.cid).all()[-1]

    total_price = 0
    for product_with_count in specified_products:
        total_price += product_with_count['product'].price * product_with_count['count']
        session.add(OrderItem(
            oid=this_order.oid,
            qty=product_with_count['count'],
            pid=product_with_count['product'].pid
        ))
        session.commit()

    print('This order is submitted: ')
    for product_with_count in specified_products:
        product = product_with_count['product']
        print(f'id: {product.pid}\tname: {product.pname}\tcount: {product_with_count["count"]}\tprice: {product.price}')
    print(f'Total Price: {total_price}')


def show_orders_and_items():
    all_orders = session.query(Order).all()
    print('\nAll orders: ')
    for order in all_orders:
        print(
            f'Order id: {order.oid}\tOrder Date: {order.oDate}\t'
            f'Customer id: {order.customer.cid}\tCustomer Name: {order.customer.cname}'
        )

    specified_order = input('Select an order id: ')
    if not specified_order.isdigit():
        print('Order id is wrong.')
        show_orders_and_items()
    this_order = session.query(Order).filter(Order.oid == specified_order).first()
    if not this_order:
        print('Order id is wrong.')
        show_orders_and_items()

    while True:
        print('\nOrder Items of This Order:')
        all_orderitems = session.query(OrderItem).filter(OrderItem.oid == this_order.oid).all()
        for orderitem in all_orderitems:
            print(
                f'id: {orderitem.iid}\tcount: {orderitem.qty}\torder id: {orderitem.oid}\tproduct id: {orderitem.pid}')

        print('\nFor adding order item enter A')
        print('For deleting order item enter D')
        print('For exiting enter E')
        this_command = input('Enter a character: ')
        if this_command == 'A':

            all_products = session.query(Product).all()
            print('\nAll Products are: ')
            for product in all_products:
                print(f'id: {product.pid}\tName: {product.pname}\tPrice: {product.price}')
            product_id = input('Enter the id of the product: ')
            product_count = input('Enter the count of the product: ')

            if not (product_count.isdigit() and product_id.isdigit()):
                print('One of the data is wrong.')
                continue
            this_product = session.query(Product).filter(Product.pid == int(product_id)).first()
            if not this_product:
                print('One of the data is wrong.')
                continue

            session.add(OrderItem(
                oid=this_order.oid,
                qty=int(product_count),
                pid=this_product.pid
            ))
            session.commit()

            print('\nOrder Item added successfully.')
            print('Order Items of This Order:')
            all_orderitems = session.query(OrderItem).filter(OrderItem.oid == this_order.oid).all()
            for orderitem in all_orderitems:
                print(
                    f'id: {orderitem.iid}\tcount: {orderitem.qty}\t'
                    f'order id: {orderitem.oid}\tproduct id: {orderitem.pid}'
                )

        elif this_command == 'D':
            orderitem_id = input('Enter the id of the order item: ')
            if not orderitem_id.isdigit():
                print('Order item id is wrong.')
                continue
            this_orderitem = session.query(OrderItem) \
                .filter(and_(OrderItem.iid == int(orderitem_id), OrderItem.oid == this_order.oid)).first()
            if not this_orderitem:
                print('Order item id is wrong.')
                continue

            session.delete(this_orderitem)
            session.commit()

            print('\nOrder Item deleted successfully.')
            print('Order Items of This Order:')
            all_orderitems = session.query(OrderItem).filter(OrderItem.oid == this_order.oid).all()
            for orderitem in all_orderitems:
                print(
                    f'id: {orderitem.iid}\tcount: {orderitem.qty}\t'
                    f'order id: {orderitem.oid}\tproduct id: {orderitem.pid}'
                )

        elif this_command == 'E':
            break


def show_products():
    all_products = session.query(Product).all()
    print('\nAll Products are: ')
    for product in all_products:
        print(f'id: {product.pid}\tName: {product.pname}\tPrice: {product.price}')
    print()


def update_which():
    print()
    print('tables:')
    print('1.customers')
    print('2.order items')
    print('3.product')
    table = input('\nselect the number of table you want to update: ')
    print()
    if table == '1':
        update_customers()
    elif table == '2':
        update_order_item()
    elif table == '3':
        update_product()
    else:
        print('You have entered a wrong number.\n')


def update_customers():
    all_customers = session.query(Customer).all()
    customer_ids = []
    print('\nAll customers: ')
    for customer in all_customers:
        customer_ids.append(customer.cid)
        print(
            f'Customer id: {customer.cid}\t'
            f'Customer name: {customer.cname}'
        )
    customer_id = input('Select a customer id: ')

    if int(customer_id) not in customer_ids:
        print("wrong id")
        print()
        return

    this_order = session.query(Customer).filter(Customer.cid == customer_id).first()
    print(
        f'Customer id: {this_order.cid}\t'
        f'Customer name: {this_order.cname}'
    )

    customer_new_name = input('enter new name: ')

    session.query(Customer).filter(Customer.cid == customer_id).update({Customer.cname: customer_new_name})
    session.commit()

    this_order = session.query(Customer).filter(Customer.cid == customer_id).first()
    print(
        f'Customer id: {this_order.cid}\t'
        f'Customer name: {this_order.cname}'
    )
    print()


def update_order_item():
    all_order_item = session.query(OrderItem).all()
    order_item_ids = []
    print('\nAll order item: ')
    for order_item in all_order_item:
        order_item_ids.append(order_item.iid)
        print(
            f'Order Item id: {order_item.iid}\t'
            f'order id: {order_item.oid}\t'
            f'product count: {order_item.qty}\t'
            f'product id: {order_item.pid}'
        )
    order_item_id = input('Select an order item id: ')
    if int(order_item_id) not in order_item_ids:
        print("wrong id")
        print()
        return

    this_order_item = session.query(OrderItem).filter(OrderItem.iid == order_item_id).first()

    print(
        f'Order Item id: {this_order_item.iid}\t'
        f'order id: {this_order_item.oid}\t'
        f'product count: {this_order_item.qty}\t'
        f'product id: {this_order_item.pid}'
    )

    order_item_new_qty = input('enter new product count: ')

    session.query(OrderItem).filter(OrderItem.iid == order_item_id).update({OrderItem.qty: order_item_new_qty})
    date = datetime.datetime.utcnow()
    session.query(Order).filter(Order.oid == this_order_item.oid).update({Order.oDate: date})
    session.commit()

    this_order_item = session.query(OrderItem).filter(OrderItem.iid == order_item_id).first()

    print(
        f'Order Item id: {this_order_item.iid}\t'
        f'order id: {this_order_item.oid}\t'
        f'product count: {this_order_item.qty}\t'
        f'product id: {this_order_item.pid}'
    )
    print()


def update_product():
    all_product = session.query(Product).all()
    product_ids = []
    print('\nAll product: ')
    for product in all_product:
        product_ids.append(product.pid)
        print(
            f'product id: {product.pid}\t'
            f'product name: {product.pname}\t'
            f'product price: {product.price}'
        )

    product_id = input('Select an product id: ')
    if int(product_id) not in product_ids:
        print('wrong id')
        print()
        return

    this_product = session.query(Product).filter(Product.pid == product_id).first()

    print(
        f'product id: {this_product.pid}\t'
        f'product name: {this_product.pname}\t'
        f'product price: {this_product.price}'
    )

    print("1.name")
    print("2.price")
    choose_command = input("which one do you want to change:")

    if choose_command == "1":
        name = input('enter new name : ')
        session.query(Product).filter(Product.pid == product_id).update({Product.pname: name})
        session.commit()

    elif choose_command == "2":
        price = input('enter new price : ')
        session.query(Product).filter(Product.pid == product_id).update({Product.price: price})
        session.commit()

    else:
        print("wrong command")
        return

    this_product = session.query(Product).filter(Product.pid == product_id).first()

    print(
        f'product id: {this_product.pid}\t'
        f'product name: {this_product.pname}\t'
        f'product price: {this_product.price}'
    )
    print()


while True:
    print('1. Create New Order')
    print('2. Show Orders and Items')
    print('3. Show Products')
    print('4. Update')
    print('5. Exit')

    command = input('Enter a number: ')

    if command == '1':
        make_new_order()
    elif command == '2':
        show_orders_and_items()
    elif command == '3':
        show_products()
    elif command == '4':
        update_which()
    elif command == '5':
        break
    else:
        print('You have entered a wrong number.\n')
