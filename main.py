import datetime

from tkinter import *
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
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


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        self.geometry("774x553+558+225")
        self.minsize(176, 1)
        self.maxsize(1924, 1050)
        self.resizable(1, 1)
        self.title("Product Manager Application")
        self.configure(background="#d9d9d9")

        self.first_frame = None
        self.welcome_label = None
        self.option_label = None
        self.show = None
        self.update = None
        self.add = None
        self.delete = None
        self.exit = None
        self.back_show_button = None
        self.show_listbox = None
        self.product_show_button = None
        self.orderitem_show_button = None
        self.order_show_button = None
        self.customer_show_button = None
        self.id_entry = None
        self.add_back_button = None
        self.add_orderitem_button = None
        self.add_order_button = None
        self.add_product_button = None
        self.add_customer_button = None
        self.add_orderitem_produtid_entry = None
        self.add_orderitem_count_entry = None
        self.add_orderitem_orderid_entry = None
        self.add_order_customerid_entry = None
        self.add_product_price_entry = None
        self.add_product_name_entry = None
        self.add_customer_name_entry = None
        self.update_back_button = None
        self.update_customer_id_entry = None
        self.update_product_id_entry = None
        self.update_order_id_entry = None
        self.update_orderitem_id_entry = None
        self.update_find_customer_button = None
        self.update_find_order_button = None
        self.update_find_product_button = None
        self.update_find_orderitem_button = None
        self.update_customer_customername_entry = None
        self.update_orderitem_product_entry = None
        self.update_product_price_entry = None
        self.update_order_customerid_entry = None
        self.update_orderitem_button = None
        self.update_order_button = None
        self.update_product_button = None
        self.update_customer_button = None
        self.update_orderitem_count_entry = None
        self.update_orderitem_orderid_entry = None
        self.update_orderitem_orderitemid_entry = None
        self.update_order_orderid_entry = None
        self.update_product_productname_entry = None
        self.update_product_productid_entry = None
        self.update_customer_customerid_entry = None
        self.delete_back_button = None
        self.delete_orderitem_button = None
        self.delete_order_button = None
        self.delete_product_button = None
        self.delete_customer_button = None
        self.delete_orderitem_id_entry = None
        self.delete_order_id_entry = None
        self.delete_product_id_entry = None
        self.delete_customer_id_entry = None

        self.home_page()

    def home_page(self):
        self.first_frame = Frame()
        self.welcome_label = Label(self.first_frame)
        self.option_label = Label(self.first_frame)
        self.show = Button()
        self.update = Button()
        self.add = Button()
        self.delete = Button()
        self.exit = Button()
        self.show_information()
        self.show_button()
        self.update_button()
        self.delete_button()
        self.add_button()
        self.exit_button()

    def clear_home_page(self):
        self.first_frame.destroy()
        self.show.destroy()
        self.add.destroy()
        self.delete.destroy()
        self.update.destroy()
        self.exit.destroy()

    def show_information(self):
        self.first_frame.place(relx=0.155, rely=0.072, relheight=0.19, relwidth=0.678)

        self.first_frame.configure(
            relief='groove',
            borderwidth="2",
            background="#d9d9d9"
        )

        self.welcome_label.place(relx=0.133, rely=0.19, height=34, width=407)
        self.welcome_label.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            text='''Welcome to The Product Manager Application'''
        )

        self.option_label.place(relx=0.21, rely=0.571, height=23, width=317)
        self.option_label.configure(
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            text='''Select One of The Options Below'''
        )

    def clear_show_page(self):
        self.back_show_button.destroy()
        self.show_listbox.destroy()
        self.product_show_button.destroy()
        self.orderitem_show_button.destroy()
        self.order_show_button.destroy()
        self.customer_show_button.destroy()
        self.id_entry.destroy()

    def show_customers_command(self):
        this_customer_id = int(self.id_entry.get())
        this_customer = session.query(Customer).filter(Customer.cid == this_customer_id).first()
        if this_customer is None:
            self.show_listbox.insert(0, 'This item does not exist.')
        else:
            self.show_listbox.insert(0, this_customer)

    def show_customers(self):
        self.customer_show_button = Button()
        self.customer_show_button.place(relx=0.155, rely=0.452, height=92, width=268)
        self.customer_show_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_customers_command,
            text='''Customers'''
        )

    def show_product_command(self):
        this_product_id = int(self.id_entry.get())
        this_product = session.query(Product).filter(Product.pid == this_product_id).first()
        if this_product is None:
            self.show_listbox.insert(0, 'This item does not exist.')
        else:
            self.show_listbox.insert(0, this_product)

    def show_product(self):
        self.product_show_button = Button()
        self.product_show_button.place(relx=0.53, rely=0.633, height=92, width=268)
        self.product_show_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_product_command,
            text='''Products'''
        )

    def show_orderitem_command(self):
        this_orderitem_id = int(self.id_entry.get())
        this_orderitem = session.query(OrderItem).filter(OrderItem.iid == this_orderitem_id).first()
        if this_orderitem is None:
            self.show_listbox.insert(0, 'This item does not exist.')
        else:
            self.show_listbox.insert(0, this_orderitem)

    def show_orderitem(self):
        self.orderitem_show_button = Button()
        self.orderitem_show_button.place(relx=0.155, rely=0.633, height=92, width=268)
        self.orderitem_show_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_orderitem_command,
            text='''Order Items'''
        )

    def show_order_command(self):
        this_order_id = int(self.id_entry.get())
        this_order = session.query(Order).filter(Order.oid == this_order_id).first()
        if this_order is None:
            self.show_listbox.insert(0, 'This item does not exist.')
        else:
            self.show_listbox.insert(0, this_order)

    def show_order(self):
        self.order_show_button = Button()
        self.order_show_button.place(relx=0.53, rely=0.452, height=92, width=268)
        self.order_show_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_order_command,
            text='''Orders'''
        )

    def show_listbox_command(self):
        self.show_listbox = Listbox()
        self.show_listbox.place(relx=0.155, rely=0.038, relheight=0.309, relwidth=0.716)
        self.show_listbox.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000"
        )

    def show_entry(self):
        self.id_entry = Entry()
        self.id_entry.place(relx=0.155, rely=0.37, height=36, relwidth=0.716)
        self.id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            insertbackground="black"
        )
        self.id_entry.insert(0, "Enter the ID")

    def show_back_command(self):
        self.clear_show_page()
        self.home_page()

    def show_back(self):
        self.back_show_button = Button()
        self.back_show_button.place(relx=0.155, rely=0.814, height=92, width=558)
        self.back_show_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_back_command,
            text='''BACK'''
        )

    def show_command(self):
        self.clear_home_page()
        self.show_customers()
        self.show_product()
        self.show_orderitem()
        self.show_order()
        self.show_listbox_command()
        self.show_entry()
        self.show_back()

    def show_button(self):
        self.show.place(relx=0.155, rely=0.307, height=92, width=228)
        self.show.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.show_command,
            text='''Show Information'''
        )

    def clear_add_page(self):
        self.add_back_button.destroy()
        self.add_orderitem_button.destroy()
        self.add_order_button.destroy()
        self.add_product_button.destroy()
        self.add_customer_button.destroy()
        self.add_orderitem_produtid_entry.destroy()
        self.add_orderitem_count_entry.destroy()
        self.add_orderitem_orderid_entry.destroy()
        self.add_order_customerid_entry.destroy()
        self.add_product_price_entry.destroy()
        self.add_product_name_entry.destroy()
        self.add_customer_name_entry.destroy()

    def add_orderitem_command(self):
        this_orderitem = OrderItem(
            oid=int(self.add_orderitem_orderid_entry.get()),
            qty=int(self.add_orderitem_count_entry.get()),
            pid=int(self.add_orderitem_produtid_entry.get())
        )
        session.add(this_orderitem)
        session.commit()

    def add_orderitem(self):
        self.add_orderitem_button = Button()
        self.add_orderitem_button.place(relx=0.788, rely=0.561, height=42, width=138)
        self.add_orderitem_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_orderitem_command,
            text='''Add Order Item'''
        )

    def add_product_command(self):
        this_product = Product(
            pname=self.add_product_name_entry.get(),
            price=int(self.add_product_price_entry.get())
        )
        session.add(this_product)
        session.commit()

    def add_product(self):
        self.add_product_button = Button()
        self.add_product_button.place(relx=0.788, rely=0.235, height=42, width=138)
        self.add_product_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_product_command,
            text='''Add Product'''
        )

    def add_order_command(self):
        this_order = Order(cid=int(self.add_order_customerid_entry.get()))
        session.add(this_order)
        session.commit()

    def add_order(self):
        self.add_order_button = Button()
        self.add_order_button.place(relx=0.788, rely=0.398, height=42, width=138)
        self.add_order_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_order_command,
            text='''Add Order'''
        )

    def add_customer_command(self):
        this_customer = Customer(cname=self.add_customer_name_entry.get())
        session.add(this_customer)
        session.commit()

    def add_customer(self):
        self.add_customer_button = Button()
        self.add_customer_button.place(relx=0.788, rely=0.072, height=42, width=138)
        self.add_customer_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_customer_command,
            text='''Add Customer'''
        )

    def add_orderitem_produtid(self):
        self.add_orderitem_produtid_entry = Entry()
        self.add_orderitem_produtid_entry.place(relx=0.478, rely=0.597, height=26, relwidth=0.199)
        self.add_orderitem_produtid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_orderitem_produtid_entry.insert(0, 'Enter Product Id')

    def add_orderitem_count(self):
        self.add_orderitem_count_entry = Entry()
        self.add_orderitem_count_entry.place(relx=0.258, rely=0.597, height=26, relwidth=0.199)
        self.add_orderitem_count_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_orderitem_count_entry.insert(0, 'Enter Count')

    def add_orderitem_orderid(self):
        self.add_orderitem_orderid_entry = Entry()
        self.add_orderitem_orderid_entry.place(relx=0.039, rely=0.597, height=26, relwidth=0.199)
        self.add_orderitem_orderid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_orderitem_orderid_entry.insert(0, 'Enter Order Id')

    def add_order_customerid(self):
        self.add_order_customerid_entry = Entry()
        self.add_order_customerid_entry.place(relx=0.039, rely=0.434, height=26, relwidth=0.199)
        self.add_order_customerid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_order_customerid_entry.insert(0, 'Enter Customer ID')

    def add_product_price(self):
        self.add_product_price_entry = Entry()
        self.add_product_price_entry.place(relx=0.258, rely=0.253, height=26, relwidth=0.199)
        self.add_product_price_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_product_price_entry.insert(0, 'Enter Product Price')

    def add_product_name(self):
        self.add_product_name_entry = Entry()
        self.add_product_name_entry.place(relx=0.039, rely=0.253, height=26, relwidth=0.199)
        self.add_product_name_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        self.add_product_name_entry.insert(0, 'Enter Product Name')

    def add_customer_name(self):
        self.add_customer_name_entry = Entry()
        self.add_customer_name_entry.place(relx=0.039, rely=0.108, height=26, relwidth=0.199)
        self.add_customer_name_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            insertbackground="black"
        )
        self.add_customer_name_entry.insert(0, 'Enter Customer Name')

    def add_back_command(self):
        self.clear_add_page()
        self.home_page()

    def add_back(self):
        self.add_back_button = Button()
        self.add_back_button.place(relx=0.155, rely=0.814, height=92, width=558)
        self.add_back_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_back_command,
            text='''BACK'''
        )

    def add_command(self):
        self.clear_home_page()
        self.add_back()
        self.add_orderitem()
        self.add_order()
        self.add_customer()
        self.add_product()
        self.add_orderitem_produtid()
        self.add_orderitem_count()
        self.add_orderitem_orderid()
        self.add_order_customerid()
        self.add_product_price()
        self.add_product_name()
        self.add_customer_name()

    def add_button(self):
        self.add.place(relx=0.155, rely=0.524, height=92, width=228)
        self.add.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.add_command,
            text='''Add Information'''
        )

    def clear_update_page(self):
        self.update_back_button.destroy()
        self.update_customer_id_entry.destroy()
        self.update_product_id_entry.destroy()
        self.update_order_id_entry.destroy()
        self.update_orderitem_id_entry.destroy()
        self.update_find_customer_button.destroy()
        self.update_find_order_button.destroy()
        self.update_find_product_button.destroy()
        self.update_find_orderitem_button.destroy()
        self.update_customer_customername_entry.destroy()
        self.update_orderitem_product_entry.destroy()
        self.update_product_price_entry.destroy()
        self.update_order_customerid_entry.destroy()
        self.update_orderitem_button.destroy()
        self.update_order_button.destroy()
        self.update_product_button.destroy()
        self.update_customer_button.destroy()
        self.update_orderitem_count_entry.destroy()
        self.update_orderitem_orderid_entry.destroy()
        self.update_orderitem_orderitemid_entry.destroy()
        self.update_order_orderid_entry.destroy()
        self.update_product_productname_entry.destroy()
        self.update_product_productid_entry.destroy()
        self.update_customer_customerid_entry.destroy()

    def update_back_command(self):
        self.clear_update_page()
        self.home_page()

    def update_back(self):
        self.update_back_button = Button()
        self.update_back_button.place(relx=0.052, rely=0.741, height=72, width=708)
        self.update_back_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_back_command,
            text='''BACK'''
        )

    def update_find_customer_command(self):
        this_customer_id = int(self.update_customer_id_entry.get())
        this_customer = session.query(Customer).filter(Customer.cid == this_customer_id).first()
        self.update_customer_customerid_entry.delete(0, 'end')
        self.update_customer_customername_entry.delete(0, 'end')
        self.update_customer_customerid_entry.insert(0, this_customer.cid)
        self.update_customer_customername_entry.insert(0, this_customer.cname)

    def update_find_customer(self):
        self.update_find_customer_button = Button()
        self.update_find_customer_button.place(relx=0.788, rely=0.036, height=42, width=138)
        self.update_find_customer_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_find_customer_command,
            text='''Find Customer'''
        )

    def update_find_order_command(self):
        this_order_id = int(self.update_order_id_entry.get())
        this_order = session.query(Order).filter(Order.oid == this_order_id).first()
        self.update_order_orderid_entry.delete(0, 'end')
        self.update_order_customerid_entry.delete(0, 'end')
        self.update_order_orderid_entry.insert(0, this_order.oid)
        self.update_order_customerid_entry.insert(0, this_order.cid)

    def update_find_order(self):
        self.update_find_order_button = Button()
        self.update_find_order_button.place(relx=0.788, rely=0.362, height=42, width=138)
        self.update_find_order_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_find_order_command,
            text='''Find Order'''
        )

    def update_find_product_command(self):
        this_product_id = int(self.update_product_id_entry.get())
        this_product = session.query(Product).filter(Product.pid == this_product_id).first()
        self.update_product_productid_entry.delete(0, 'end')
        self.update_product_productname_entry.delete(0, 'end')
        self.update_product_price_entry.delete(0, 'end')
        self.update_product_productid_entry.insert(0, this_product.pid)
        self.update_product_productname_entry.insert(0, this_product.pname)
        self.update_product_price_entry.insert(0, this_product.price)

    def update_find_product(self):
        self.update_find_product_button = Button()
        self.update_find_product_button.place(relx=0.788, rely=0.199, height=42, width=138)
        self.update_find_product_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_find_product_command,
            text='''Find Product'''
        )

    def update_find_orderitem_command(self):
        this_orderitem_id = int(self.update_orderitem_id_entry.get())
        this_orderitem = session.query(OrderItem).filter(OrderItem.iid == this_orderitem_id).first()
        self.update_orderitem_orderitemid_entry.delete(0, 'end')
        self.update_orderitem_orderid_entry.delete(0, 'end')
        self.update_orderitem_count_entry.delete(0, 'end')
        self.update_orderitem_product_entry.delete(0, 'end')
        self.update_orderitem_orderitemid_entry.insert(0, this_orderitem.iid)
        self.update_orderitem_orderid_entry.insert(0, this_orderitem.oid)
        self.update_orderitem_count_entry.insert(0, this_orderitem.qty)
        self.update_orderitem_product_entry.insert(0, this_orderitem.pid)

    def update_find_orderitem(self):
        self.update_find_orderitem_button = Button()
        self.update_find_orderitem_button.place(relx=0.788, rely=0.524, height=42, width=138)
        self.update_find_orderitem_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_find_orderitem_command,
            text='''Find Order Item'''
        )

    def update_order_command(self):
        this_order_id = int(self.update_order_orderid_entry.get())
        session.query(Order).filter(Order.oid == this_order_id).update({
            Order.cid: int(self.update_order_customerid_entry.get()),
            Order.oDate: datetime.datetime.utcnow()
        })

    def update_order(self):
        self.update_order_button = Button()
        self.update_order_button.place(relx=0.788, rely=0.434, height=42, width=138)
        self.update_order_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_order_command,
            text='''Update Order'''
        )

    def update_product_command(self):
        this_product_id = int(self.update_product_productid_entry.get())
        session.query(Product).filter(Product.pid == this_product_id).update({
            Product.pname: self.update_product_productname_entry.get(),
            Product.price: int(self.update_product_price_entry.get()),
        })

    def update_product(self):
        self.update_product_button = Button()
        self.update_product_button.place(relx=0.788, rely=0.271, height=42, width=138)
        self.update_product_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_product_command,
            text='''Update Product'''
        )

    def update_orderitem_command(self):
        this_orderitem_id = int(self.update_orderitem_orderitemid_entry.get())
        session.query(OrderItem).filter(OrderItem.iid == this_orderitem_id).update({
            OrderItem.pid: int(self.update_orderitem_product_entry.get()),
            OrderItem.oid: int(self.update_orderitem_orderid_entry.get()),
            OrderItem.qty: int(self.update_orderitem_count_entry.get())
        })

    def update_orderitem(self):
        self.update_orderitem_button = Button()
        self.update_orderitem_button.place(relx=0.788, rely=0.597, height=42, width=138)
        self.update_orderitem_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_orderitem_command,
            text='''Update Order Item'''
        )

    def update_customer_command(self):
        this_customer_id = int(self.update_customer_customerid_entry.get())
        session.query(Customer).filter(Customer.cid == this_customer_id).update({
            Customer.cname: self.update_customer_customername_entry.get(),
        })

    def update_customer(self):
        self.update_customer_button = Button()
        self.update_customer_button.place(relx=0.788, rely=0.108, height=42, width=138)
        self.update_customer_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_customer_command,
            text='''Update Customer'''
        )

    def update_customer_id(self):
        self.update_customer_id_entry = Entry()
        self.update_customer_id_entry.place(relx=0.039, rely=0.054, height=26, relwidth=0.199)
        self.update_customer_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        
    def update_product_id(self):
        self.update_product_id_entry = Entry()
        self.update_product_id_entry.place(relx=0.039, rely=0.199, height=26, relwidth=0.199)
        self.update_product_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        
    def update_order_id(self):
        self.update_order_id_entry = Entry()
        self.update_order_id_entry.place(relx=0.039, rely=0.38, height=26, relwidth=0.199)
        self.update_order_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        
    def update_orderitem_id(self):
        self.update_orderitem_id_entry = Entry()
        self.update_orderitem_id_entry.place(relx=0.039, rely=0.542, height=26, relwidth=0.199)
        self.update_orderitem_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        
    def update_customer_customername(self):
        self.update_customer_customername_entry = Entry()
        self.update_customer_customername_entry.place(relx=0.258, rely=0.108, height=26, relwidth=0.199)
        self.update_customer_customername_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_orderitem_product(self):
        self.update_orderitem_product_entry = Entry()
        self.update_orderitem_product_entry.place(relx=0.039, rely=0.651, height=26, relwidth=0.199)
        self.update_orderitem_product_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )
        
    def update_product_price(self):
        self.update_product_price_entry = Entry()
        self.update_product_price_entry.place(relx=0.478, rely=0.253, height=26, relwidth=0.199)
        self.update_product_price_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_order_customerid(self):
        self.update_order_customerid_entry = Entry()
        self.update_order_customerid_entry.place(relx=0.258, rely=0.434, height=26, relwidth=0.199)
        self.update_order_customerid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_orderitem_count(self):
        self.update_orderitem_count_entry = Entry()
        self.update_orderitem_count_entry.place(relx=0.478, rely=0.597, height=26, relwidth=0.199)
        self.update_orderitem_count_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_orderitem_orderid(self):
        self.update_orderitem_orderid_entry = Entry()
        self.update_orderitem_orderid_entry.place(relx=0.258, rely=0.597, height=26, relwidth=0.199)
        self.update_orderitem_orderid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_orderitem_orderitemid(self):
        self.update_orderitem_orderitemid_entry = Entry()
        self.update_orderitem_orderitemid_entry.place(relx=0.039, rely=0.597, height=26, relwidth=0.199)
        self.update_orderitem_orderitemid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_order_orderid(self):
        self.update_order_orderid_entry = Entry()
        self.update_order_orderid_entry.place(relx=0.039, rely=0.434, height=26, relwidth=0.199)
        self.update_order_orderid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_product_productname(self):
        self.update_product_productname_entry = Entry()
        self.update_product_productname_entry.place(relx=0.258, rely=0.253, height=26, relwidth=0.199)
        self.update_product_productname_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_product_productid(self):
        self.update_product_productid_entry = Entry()
        self.update_product_productid_entry.place(relx=0.039, rely=0.253, height=26, relwidth=0.199)
        self.update_product_productid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def update_customer_customerid(self):
        self.update_customer_customerid_entry = Entry()
        self.update_customer_customerid_entry.place(relx=0.039, rely=0.108, height=26, relwidth=0.199)
        self.update_customer_customerid_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            insertbackground="black"
        )

    def update_command(self):
        self.clear_home_page()
        self.update_back()
        self.update_customer()
        self.update_customer_customerid()
        self.update_customer_customername()
        self.update_customer_id()
        self.update_find_customer()
        self.update_find_order()
        self.update_find_orderitem()
        self.update_find_product()
        self.update_order()
        self.update_order_id()
        self.update_order_customerid()
        self.update_order_orderid()
        self.update_orderitem()
        self.update_orderitem_count()
        self.update_orderitem_id()
        self.update_orderitem_orderid()
        self.update_orderitem_product()
        self.update_orderitem_orderitemid()
        self.update_product()
        self.update_product_id()
        self.update_product_price()
        self.update_product_productid()
        self.update_product_productname()

    def update_button(self):
        self.update.place(relx=0.543, rely=0.307, height=92, width=228)
        self.update.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.update_command,
            text='''Update Information'''
        )

    def delete_back_command(self):
        self.delete_back_button.destroy()
        self.delete_orderitem_button.destroy()
        self.delete_order_button.destroy()
        self.delete_product_button.destroy()
        self.delete_customer_button.destroy()
        self.delete_orderitem_id_entry.destroy()
        self.delete_order_id_entry.destroy()
        self.delete_product_id_entry.destroy()
        self.delete_customer_id_entry.destroy()
        self.home_page()

    def delete_back(self):
        self.delete_back_button = Button()
        self.delete_back_button.place(relx=0.052, rely=0.741, height=72, width=708)
        self.delete_back_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_back_command,
            text='''BACK'''
        )

    def delete_orderitem_command(self):
        this_orderitem_id = int(self.delete_orderitem_id_entry.get())
        this_orderitem = session.query(OrderItem).filter(OrderItem.iid == this_orderitem_id).first()
        session.delete(this_orderitem)

    def delete_orderitem(self):
        self.delete_orderitem_button = Button()
        self.delete_orderitem_button.place(relx=0.788, rely=0.579, height=42, width=138)
        self.delete_orderitem_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_orderitem_command,
            text='''Delete Order Item'''
        )

    def delete_order_command(self):
        this_order_id = int(self.delete_order_id_entry.get())
        this_order = session.query(Order).filter(Order.oid == this_order_id).first()
        session.delete(this_order)

    def delete_order(self):
        self.delete_order_button = Button()
        self.delete_order_button.place(relx=0.788, rely=0.416, height=42, width=138)
        self.delete_order_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_order_command,
            text='''Delete Order'''
        )

    def delete_product_command(self):
        this_product_id = int(self.delete_product_id_entry.get())
        this_product = session.query(Product).filter(Product.pid == this_product_id).first()
        session.delete(this_product)

    def delete_product(self):
        self.delete_product_button = Button()
        self.delete_product_button.place(relx=0.788, rely=0.253, height=42, width=138)
        self.delete_product_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_product_command,
            text='''Delete Product'''
        )

    def delete_customer_command(self):
        this_customer_id = int(self.delete_customer_id_entry.get())
        this_customer = session.query(Customer).filter(Customer.cid == this_customer_id).first()
        session.delete(this_customer)

    def delete_customer(self):
        self.delete_customer_button = Button()
        self.delete_customer_button.place(relx=0.788, rely=0.09, height=42, width=138)
        self.delete_customer_button.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_customer_command,
            text='''Delete Customer'''
        )

    def delete_orderitem_id(self):
        self.delete_orderitem_id_entry = Entry()
        self.delete_orderitem_id_entry.place(relx=0.039, rely=0.597, height=26, relwidth=0.199)
        self.delete_orderitem_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def delete_order_id(self):
        self.delete_order_id_entry = Entry()
        self.delete_order_id_entry.place(relx=0.039, rely=0.434, height=26, relwidth=0.199)
        self.delete_order_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def delete_product_id(self):
        self.delete_product_id_entry = Entry()
        self.delete_product_id_entry.place(relx=0.039, rely=0.271, height=26, relwidth=0.199)
        self.delete_product_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="blue",
            selectforeground="white"
        )

    def delete_customer_id(self):
        self.delete_customer_id_entry = Entry()
        self.delete_customer_id_entry.place(relx=0.039, rely=0.108, height=26, relwidth=0.199)
        self.delete_customer_id_entry.configure(
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            insertbackground="black"
        )

    def delete_command(self):
        self.clear_home_page()
        self.delete_back()
        self.delete_orderitem()
        self.delete_order()
        self.delete_product()
        self.delete_customer()
        self.delete_orderitem_id()
        self.delete_order_id()
        self.delete_product_id()
        self.delete_customer_id()

    def delete_button(self):
        self.delete.place(relx=0.543, rely=0.524, height=92, width=228)
        self.delete.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.delete_command,
            text='''Delete Information'''
        )

    def exit_command(self):
        self.destroy()
        self.quit()

    def exit_button(self):
        self.exit.place(relx=0.155, rely=0.741, height=92, width=528)
        self.exit.configure(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0",
            command=self.exit_command,
            text='''EXIT'''
        )


root = Root()
root.mainloop()
