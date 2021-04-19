import config
#import config module for database connection
from tabulate import tabulate
#import tabulate module for displaying tables

con = config.con
cur = con.cursor()
#sqlite connection and cursor variables


class Customer:
    """Customer class which has attributes for username, saved address, and saved payment method.
    When customer object is created, the username attribute is set to the username passed in,
    and the address and payment_method attributes are set to the customer values stored
     in the 'customers' table in the database."""

    def __init__(self, username):
        self.username = username

        self.address = cur.execute("""SELECT address FROM customers WHERE username = ?""",
                                   (self.username,)).fetchone()[0]

        self.payment_method = cur.execute("""SELECT payment FROM customers WHERE username = ?""",
                                          (self.username,)).fetchone()[0]

    def update_address(self, new_address):
        """method to update customer address saved in 'customers' table and
        then assign this new value to the address attribute."""

        cur.execute("""UPDATE customers SET address = ? WHERE username = ?""",
                    (new_address, self.username))

        self.address = cur.execute("""SELECT address FROM customers WHERE username = ?""",
                                   (self.username,)).fetchone()[0]

    def update_payment(self, new_payment):
        """method to update the customer saved payment method in 'customers' table and
        then assign this new value to the payment_method attribute."""

        cur.execute("""UPDATE customers SET payment = ? WHERE username = ?""",
                    (new_payment, self.username))

        self.payment_method = cur.execute("""SELECT payment FROM customers WHERE username = ?""",
                                          (self.username,)).fetchone()[0]


class Basket:
    """Basket class which has attributes for the basket's contents, total items in basket,
    and the current subtotal."""

    def __init__(self):
        self.contents = []
        self.total_items = 0
        self.subtotal = 0

    def add_item(self, item):
        """Method to add an item to the basket. It takes a BasketItem object and adds it to the contents attribute.
        It also then updates the total_items and subtotal attributes to reflect the change."""

        self.contents.append(item)
        self.update_total_items()
        self.update_subtotal()

    def remove_item(self, product_id):
        """Method to remove an item form the basket. This method takes a product id and then iterates
         over the basket contents list to remove any BasketItem in it with the matching productid.
         The total_items and subtotal attributes are then updated to reflect the changes."""

        for item in self.contents:
            if item.productid == product_id:
                self.contents.remove(item)

        self.update_total_items()
        self.update_subtotal()

    def view_basket(self):
        """This method allows the basket contents to be printed in a table to be viewed by the user. This method
        iterates over the basket contents and appends the productid, product_name, quantity_in_basket,
        and subtotal attributes for each BasketItem object in it to the data list. It then appends a blank line and
        a total line to the data list. This list is then printed using the tabulate module."""

        data = []
        for i in self.contents:
            data.append([i.productid, i.product_name, i.quantity_in_basket, i.subtotal])

        data.append(['', '', '', ''])
        data.append(['', '', "Total =", self.subtotal])

        print(tabulate(data, headers=["Product ID", "Name", "Quantity", "Subtotal"]))

    def update_total_items(self):
        """This method iterates over the basket contents list and adds the quantity_in_basket attribute of each
        BasketItem to the new_total variable. The total_items attribute is then set to new_total."""

        new_total = 0

        for i in self.contents:
            new_total += i.quantity_in_basket

        self.total_items = new_total

    def update_subtotal(self):
        """This method iterates over the basket contents list and adds the subtotal attribute of each BasketItem
         to the new_subtotal variable. The subtotal attribute of the Basket is then set to new_subtotal."""

        new_subtotal = 0

        for i in self.contents:
            new_subtotal += i.subtotal

        self.subtotal = new_subtotal


class BasketItem:
    """BasketItem class which takes variables for the product id and the quantity to be added to the basket.
    The productid attribute is then used to the values for the vendor_name, product_name, unit_cost, and location
     from the 'catalogue' table.
     vendor_type attribute is pulled from the 'vendors' table using the vendor_name attribute.
     subtotal attribute is assigned by multiplying unit_cost and quantity_in_basket."""

    def __init__(self, productid, quantity_in_basket):
        self.productid = productid

        self.vendor_name = cur.execute("""SELECT vendorname FROM catalogue WHERE productid = ?""",
                                       (self.productid,)).fetchone()[0]

        self.vendor_type = cur.execute("""SELECT vendortype FROM vendors WHERE vendorname = ?""",
                                       (self.vendor_name,)).fetchone()[0]

        self.product_name = cur.execute("""SELECT productname FROM catalogue WHERE productid = ?""",
                                        (self.productid,)).fetchone()[0]

        self.unit_cost = cur.execute("""SELECT unitcost FROM catalogue WHERE productid = ?""",
                                     (self.productid,)).fetchone()[0]

        self.location = cur.execute("""SELECT location FROM catalogue WHERE productid = ?""",
                                    (self.productid,)).fetchone()[0]

        self.quantity_in_basket = quantity_in_basket
        self.subtotal = self.unit_cost * self.quantity_in_basket

    def update_quantity(self, new_quantity):
        """This method updates the quantity_in_basket attribute and then also
        calculates the new BasketItem subtotal."""

        self.quantity_in_basket = new_quantity
        self.subtotal = self.unit_cost * self.quantity_in_basket


class Order:
    """Order class which takes a Customer object and a Basket object.
    The customer attribute is set as the Customer object.
    A new order is inserted into the 'orders' table using order_state, customer.customer_name, delivery_address,
    and delivery_method as the values inserted.
    orderid attribute is then set to the value pulled from the table row just created."""

    def __init__(self, customer, basket):
        self.customer = customer
        self.basket = basket
        self.delivery_address = ""  #initially set as blank for orderid assignment
        self.order_state = "processing"  #order state is proccessing as required by spec.
        self.delivery_method = ""  #Initially set as blank for orderid assignment

        cur.execute("""INSERT INTO orders(state, customer, address, deliverymethod) VALUES (?, ?, ?, ?)""",
                    (self.order_state, self.customer.username, self.delivery_address, self.delivery_method))

        self.orderid = cur.execute(
            """SELECT orderid FROM orders WHERE state = ? AND customer = ? AND address = ? AND deliverymethod = ?""",
            (self.order_state, self.customer.username, self.delivery_address, self.delivery_method)).fetchone()[0]

        self.payment_method = ""  #initially set as blank. Assigned new value by make_payment()
        self.delivery_method = ""  #initially set as blank. Assigned new value by choose_delivery_method()
        self.delivery_cost = 0  #Default is 0. Assigned new value if nessecary by choose_delivery_method()
        self.subtotal = self.delivery_cost + self.basket.subtotal

        """Iterates over the basket contents and adds vendor_type attribute of each object to self.x
         First party vendor products have vendor_type = 1, all other products have vendor_type = 0.
         Therefore number of BasketItems in contents == self.x if and only if all items are sold by first party.
         If all items are first party then courier shipping is available."""

        self.x = 0

        for item in self.basket.contents:
            if item.vendor_type == 1:
                self.x += 1

        if self.x == len(self.basket.contents):
            self.available_delivery_methods = ['standard', 'courier']

        else:
            self.available_delivery_methods = ['standard']

    def choose_delivery_method(self, method):
        """This method takes the chosen delivery method and sets the object delivery_method to it.
        Then depending on the chosen method, updates the delivery cost and updates the
        delivery method in the 'orders' table. The order subtotal is then printed.

        The interface currently only allows the input to be either 'standard' or 'courier'."""

        self.delivery_method = method

        if self.delivery_method == "standard":
            self.delivery_cost = 0  #arbitrary costs for demonstration purposes

            cur.execute("""UPDATE orders SET deliverymethod = ? WHERE orderid = ?""",
                        (self.delivery_method, self.orderid))

        elif self.delivery_method == "courier":
            self.delivery_cost = 5  #arbitrary costs for demonstration purposes
            self.subtotal = self.delivery_cost + self.basket.subtotal

            cur.execute("""UPDATE orders SET deliverymethod = ? WHERE orderid = ?""",
                        (self.delivery_method, self.orderid))

        print("Order Subtotal: ", str(self.subtotal))

    def choose_address(self, address):
        """This method sets the delivery_address attribute to the string passed into it.
        It also then updates the order address in 'orders' table"""

        self.delivery_address = address

        cur.execute("""UPDATE orders SET address = ? WHERE orderid = ?""",
                    (self.delivery_address, self.orderid))

    def make_payment(self, pay_type):
        """This method will initiate the payment process. In it's current state only takes a string as
        input and then sets the payment_method attribute to it, and updates the order_state attribute twice, along
        with the state value in the 'orders' table."""

        self.payment_method = pay_type
        self.order_state = "pending payment"  #order state as required in spec.

        cur.execute("""UPDATE orders SET state = ? WHERE orderid = ?""",
                    (self.order_state, self.orderid))

        """An OnlinePayment object should be instantiated here to deal with payments."""

        self.order_state = "awaiting picking"  #order state as required in spec.

        cur.execute("""UPDATE orders SET state = ? WHERE orderid = ?""",
                    (self.order_state, self.orderid))

        """Once the payment is completed, the for loop iterates over the contents of the order and 
        appends [order id, product id, product name, quantity, warehouse location] to the 
        order_items list for each item. This list is then used to insert this data into the 'orderitems' table."""

        order_items = []
        for item in self.basket.contents:
            order_items.append((self.orderid, item.productid, item.product_name,
                                item.quantity_in_basket, item.location))

        cur.executemany("""INSERT INTO orderitems VALUES (?, ?, ?, ?, ?)""", order_items)

        """Payment confirmed printed, and changes committed to database."""

        print("Payment Confirmed")

        con.commit()

        """Option to save """

        if self.payment_method != self.customer.payment_method:
            x = str(input("Update saved payment method?: y/n\n>>"))
            if x == 'y':
                self.customer.update_payment(self.payment_method)

    def apply_promo(self, promo):
        """Placeholder method for applying promo codes to the order.
        Would take promo code, verify it, and apply reduction to self.subtotal."""
        pass


class Payment:
    """This is merely a placeholder class which can be filled out at a later date
    with the real functionality to process payments."""
    pass
