import config
#import config module for database connection
from tabulate import tabulate
#import tabulate module for displaying tables

con = config.con
cur = con.cursor()
#sqlite connection and cursor variables


class Vendor:
    """Vendor class which pulls has attributes for the vendor name and type. Vendor type is pulled from
    the 'vendors' table in the database using the vendor name."""

    def __init__(self, vendorname):
        self.vendorname = vendorname
        self.vendor_type = cur.execute("""SELECT vendortype FROM vendors WHERE vendorname = ?""",
                                       (self.vendorname,)).fetchone()[0]

    def add_product(self, name, cost, stock, location):
        """Inserts a new product into the catalogue using the variables passed in."""

        cur.execute("""INSERT INTO catalogue(vendorname, productname, unitcost, stock, location) 
                        VALUES (?, ?, ?, ?, ?)""", (self.vendorname, name, cost, stock, location))

    def remove_product(self, product_id):
        """This method removes a product from the catalogue providing that the
        product selected is sold by the vendor.
        This is checked by the WHERE clause."""

        cur.execute("""DELETE FROM catalogue WHERE productid = ? AND vendorname = ?""",
                    (product_id, self.vendorname))

    def show_catalogue(self):
        """This method prints all the products in the catalogue sold by the vendor using tabulate."""

        data = cur.execute("""SELECT productid, productname, unitcost, stock, location 
                                FROM catalogue WHERE vendorname = ?""", (self.vendorname,)).fetchall()
        print(tabulate(data, headers=["Product ID", "Name", "Unit Cost", "Stock", "Location"]))

    def show_orders(self):
        """This method prints all orders from the 'orders' table using tabulate."""

        data = cur.execute("""SELECT * FROM orders""").fetchall()
        print(tabulate(data, headers=["Order ID", "Status", "Customer", "Address", "Delivery Method"]))

    def show_order_detail(self, order_id):
        """This method prints the details of the order with the order_id that is passed into it."""

        data = cur.execute("""SELECT productid, productname, quantity, location FROM orderitems WHERE orderid = ?""",
                           (order_id,)).fetchall()
        print(tabulate(data, headers=["Product ID", "Name", "Quantity", "Location"]))

    def update_order_state(self, orderid, new_state):
        """Method to update an order's state. Takes and order id and the new state and
        updates them in the 'orders' table."""

        cur.execute("""UPDATE orders SET state = ? WHERE orderid = ?""",
                    (new_state, orderid))

    def update_stock(self, productid, new_stock):
        """Method to update the stock of any item sold by the vendor. Checks the product id and vendor name,
         and updates the stock in the 'catalogue'."""

        cur.execute("""UPDATE catalogue SET stock = ? WHERE productid = ? AND vendorname = ?""",
                    (new_stock, productid, self.vendorname))
