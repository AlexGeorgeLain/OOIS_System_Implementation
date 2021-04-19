import config

con = config.con
cur = con.cursor()

"""This file is used to create the test database using sqlite. It contains functions for generating the various
tables used and inserting dummy data into them for non-destructive testing"""


def create_customers():
    cur.execute("""CREATE TABLE customers
                    (
                    username text NOT NULL PRIMARY KEY,
                    address text,
                    payment text
                    )
                """)

    customer_list = [('testuser', 'Test User Lane', 'card'),
                     ('user123', '123 House', '3rd party'),
                     ]

    cur.executemany("""INSERT INTO customers VALUES (?, ?, ?)""", customer_list)


def create_vendors():
    cur.execute("""CREATE TABLE vendors
                    (
                    vendorname text NOT NULL PRIMARY KEY,
                    vendortype int
                    )
                """)

    vendor_list = [('firstpartyvendor', 1),
                   ('vendor123', 0),
                   ]

    cur.executemany("""INSERT INTO vendors VALUES (?, ?)""", vendor_list)


def create_catalogue():
    cur.execute("""CREATE TABLE catalogue
                    (
                    productid INTEGER PRIMARY KEY AUTOINCREMENT,
                    vendorname text NOT NULL,
                    productname text NOT NULL,
                    unitcost real NOT NULL,
                    stock int NOT NULL,
                    location text
                    )
                """)

    product_list = [('firstpartyvendor', 'apple', 1.00, 10, 'a1'),
                    ('firstpartyvendor', 'orange', 2.50, 12, 'a2'),
                    ('firstpartyvendor', 'banana', 3.00, 8, 'a3'),
                    ('firstpartyvendor', 'pear', 4.24, 8, 'a4'),
                    ('firstpartyvendor', 'grapefruit', 6.17, 8, 'a5'),
                    ('firstpartyvendor', 'papaya', 1.20, 8, 'a6'),

                    ('vendor123', 'knife', 8.00, 0, 'b1'),
                    ('vendor123', 'fork', 11.00, 23, 'b2'),
                    ('vendor123', 'spoon', 13.00, 19, 'b3'),
                    ('vendor123', 'bowl', 20.00, 19, 'b5'),
                    ('vendor123', 'plate', 18.30, 19, 'b6'),
                    ('vendor123', 'mug', 16.40, 19, 'b7'),
                    ('vendor123', 'glass', 7.00, 19, 'b8'), ]

    cur.executemany("""INSERT INTO catalogue(vendorname, productname, unitcost, stock, location) 
                        VALUES (?, ?, ?, ?, ?)""", product_list)


def create_orders():
    cur.execute("""CREATE TABLE orders
                        (
                        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
                        state text,
                        customer text,
                        address text,
                        deliverymethod text
                        )
                    """)

    order_list = [('awaiting picking', 'testuser', '123 Test Lane', 'standard'), ]

    cur.executemany("""INSERT INTO orders(state, customer, address, deliverymethod) 
                           VALUES (?, ?, ?, ?)""", order_list)


def create_order_items():
    cur.execute("""CREATE TABLE orderitems
                            (
                            orderid int,
                            productid int,
                            productname text,
                            quantity int,
                            location text
                            )
                        """)
    order_items_list = [(1, 1, 'apple', 3, 'a1'), ]

    cur.executemany("""INSERT INTO orderitems VALUES (?, ?, ?, ?,?)""", order_items_list)

def build_db():
    create_customers()
    create_vendors()
    create_catalogue()
    create_orders()
    create_order_items()
