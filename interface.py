import config
#import config module for database connection
import customers
import vendors
import search
#customers, vendors, and search for the user classes and search functions
from tabulate import tabulate
#import tabulate module for displaying tables

con = config.con
cur = con.cursor()
#sqlite connection and cursor variables

username_list_raw = cur.execute("""SELECT username FROM customers""").fetchall()
vendorname_list_raw = cur.execute("""SELECT vendorname FROM vendors""").fetchall()
product_list_raw = cur.execute("""SELECT productid FROM catalogue""").fetchall()
# username, vendorname, and productid as list of tuples

item_number = 0  # icreases by one each time item added to basket
item_list = []  # list of placeholder items to assign BasketItem objects in place of
                # i.e. item_list[item_number] =  BasketItem, item_number +=1

username_list = []
vendorname_list = []
product_list = []
# username, vendorname, and productid lists for validating search and login against

def create_lists():
    """Fills above lists. Makes single item lists rather than list of tuples."""

    global item_number, item_list, username_list, vendorname_list, product_list, username_list_raw,\
        vendorname_list_raw, product_list_raw

    for i in range(1, 1000):
        item_list.append('item' + str(i))

    for i in username_list_raw:
        username_list.append(i[0])

    for i in vendorname_list_raw:
        vendorname_list.append(i[0])

    for i in product_list_raw:
        product_list.append(i[0])


user = ''
user_basket = ''
user_order = ''
# creation of global variables used throughout interface functions.

create_lists()

# 'cancel' is available in all functions which will call quit() if input by the user

def start():
    """initial launcher. Runs appropriate function based on input string."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    print("Welcome to OnlineShopping.\nType cancel at anytime to close.")
    user_type = str(input("Are you a customer or a vendor?: customer/vendor\n>>"))

    if user_type == 'customer':
        customer_int()

    elif user_type == 'vendor':
        vendor_int()

    elif user_type == 'cancel':
        quit()

    else:
        print("Please type 'customer' or 'vendor'")
        start()


def customer_int():
    """Asks if new customer. Runs appropriate function based on input string. Recursive if invalid user input"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    x = str(input("Are you an existing user?: y/n\n>>"))

    if x == 'y':
        customer_login()

    elif x == 'n':
        customer_create_account()

    elif x == 'cancel':
        quit()

    else:
        customer_int()


def customer_login():
    """If the input username is in the username_list above then this function creates
     a Customer and a Basket object and calls customer_options().

     If the username is not in the list then it calls customer_int() again."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    username = str(input("Please enter username:\n>>"))

    if username in username_list:
        user = customers.Customer(username)
        user_basket = customers.Basket()
        customer_options()

    elif username == 'cancel':
        quit()

    else:
        print("Username not found")
        customer_int()


def customer_create_account():
    """Checks if the input username is in the username_list. If so the function will call itself
     and tell the user the name is taken.

     If the username is available then a new line is inserted into the 'customers' table containing the username,
     and the change is committed. Customer and Basket objects are then instantiated, before
     calling customer_options()"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list
    username = str(input("Please enter a new username:\n>>"))

    if username in username_list:
        print("Username already taken.")
        customer_create_account()

    elif username == 'cancel':
        quit()

    else:
        cur.execute("""INSERT INTO customers VALUES (?, ?, ?)""",
                    (username, '', ''))
        con.commit()

        print("User account created.")
        user = customers.Customer(username)
        user_basket = customers.Basket()
        customer_options()


def customer_options():
    """Generates a list of commands and their descriptions and prints it using the tabulate module.
    Then calls customer_main()"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list
    options = [("search", "Search product catalogue for items by name."),
               ("all", "Show all products in catalogue."),
               ("add", "Add item to basket."),
               ("remove", "Remove item from basket."),
               ("basket", "Display basket."),
               ("checkout", "Proceed to checkout."),
               ("commands", "Displays commands."),
               ("cancel", "Cancel transaction.")
               ]
    print(tabulate(options, headers=["Command", "Description"]))
    customer_main()


def customer_main():
    """Takes user input and executes one the commands shown in the options.
    This function calls itself again after all input except 'cancel' and 'checkout'."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list
    user_input = str(input("Please enter a command:\n>>"))

    if user_input == 'search':  # executes search using the search_catalogue() function from search module
        search_term = str(input("Enter search term:\n>>"))
        search.search_catalogue(search_term)
        customer_main()

    elif user_input == 'all':  #  calls show_all_products() from thw search module to display e
        search.show_all_products()
        customer_main()

    elif user_input == 'add':
        prod_id = int(input("Enter Product ID:\n>>"))  # product id to be passed to BasketItem

        prod_stock = cur.execute("""SELECT stock FROM catalogue WHERE productid = ?""",
                                 (prod_id, )).fetchone() [0]

        # checks if product is in stock
        if prod_stock == 0:
            print("Product currently unavailable. Out of stock.")
            customer_main()

        #  if statement to check if product id is valid
        if prod_id in product_list:
            quant = int(input("Enter quantity:\n>>"))  #  quantity to be passed to BasketItem
            item_list[item_number] = customers.BasketItem(prod_id, quant)  # instantiate BasketItem at
                                                                            # position in item_list
            user_basket.add_item(item_list[item_number])  # add BasketItem to basket
            item_number += 1

        else:
            print("Please use a valid Product ID.")

        customer_main()

    elif user_input == 'remove':
        prod_id = int(input("Enter Product ID:\n>>"))  # product id to be removed
        basket_ids = []

        for i in user_basket.contents:  # create list of product ids of items in basket
            basket_ids.append(i.productid)

        if prod_id in basket_ids: #  removes item if input product id matches id in basket
            user_basket.remove_item(prod_id)

        else:
            print("Please enter a valid Product ID from basket.")

        customer_main()

    elif user_input == 'basket':
        user_basket.view_basket()  # prints basket as table
        customer_main()

    elif user_input == 'checkout':
        user_order = customers.Order(user, user_basket)  # instantiates Order object and calls checkout function
        customer_checkout()

    elif user_input == 'commands':
        customer_options()  # displays available commands

    elif user_input == 'cancel':
        quit()

    else:  #  any other input calls main again
        print("Please enter a valid command. Type 'commands' to see a list of available commands.")
        customer_main()


def customer_checkout():
    """The checkout process. Calls functions to complete order and commits changes to database once complete.
    Also displays confirmation and order id to user."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    customer_delivery_address()
    customer_delivery_method()
    customer_promo()
    customer_pay()
    con.commit()

    print("Order complete.")
    print("Order ID: " + str(user_order.orderid))

    customer_continue()


def customer_delivery_address():
    """Calls different functions depending if the user has a saved address or not."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    if user.address != '':
        customer_has_address()

    else:
        customer_new_address()


def customer_has_address():
    """Allows user to either use saved address or enter new address"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    print("Saved address: " + user.address)  # display current saved address
    x = str(input("Would you like to use your saved address for delivery?: y/n\n>>"))

    if x == 'y':
        user_order.choose_address(user.address)  # uses saved address for delivery

    elif x == 'n':
        customer_new_address()  # for entering new address

    elif x == 'cancel':
        quit()

    else:
        print("please respond with y or n.")


def customer_new_address():
    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    new_address = str(input("Please enter new address, separate address lines with commas (,):\n>>"))

    if new_address == 'cancel':
        quit()

    user_order.choose_address(new_address)  # assigns new order address using Order method
    save_new = str(input("Save new address?: y/n\n>>"))

    if save_new == 'y':
        user.update_address(new_address)  # saves new address to database

    elif save_new == 'cancel':
        quit()

    else:
        pass


def customer_delivery_method():
    """Choose delivery method from methods available as determined by available_delivery_methods attribute"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    # shows available methods list
    x = str(input("Please choose delivery method: " + str(user_order.available_delivery_methods) + "\n>>"))

    # if the input is in the available list then calls choose_delivery_method method
    if x in user_order.available_delivery_methods:
        user_order.choose_delivery_method(x)

    elif x == 'cancel':
        quit()

    else:  # recursive if input deilvery method not available
        print("Please choose valid delivery method.")
        customer_delivery_method()


def customer_promo():
    """Placeholder function for customers applying promo codes to order"""
    pass


def customer_pay():
    """Calls relevant function depending on if the user has a saved payment method already"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    if user.payment_method != '':
        customer_has_payment()

    else:
        customer_new_payment()


def customer_has_payment():
    """Allows user to either use save payment method or enter a new one."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    # print saved payment method
    print("Saved payment method: " + user.payment_method)
    x = str(input("Would you like to use your saved payment method?: y/n\n>>"))

    if x == 'y':
        user_order.make_payment(user.payment_method)  # calls Order make_payment method

    elif x == 'n':
        customer_new_payment()  # new payment function

    elif x == 'cancel':
        quit()

    else:  # recursive if invalid response
        print("please respond with y or n.")
        customer_has_payment()


def customer_new_payment():
    """Allows user to enter new payment method"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    # payment method option
    new_pay = str(input("Please select payment method: card/gift card/third party \n>>"))

    # calls make_payment() method if input was valid
    if new_pay == 'card' or new_pay == 'gift card' or new_pay == 'third party':
        user_order.make_payment(new_pay)

    elif new_pay == 'cancel':
        quit()

    else: # recursive if invalid response
        print("Please respond with valid payment method.")
        customer_new_payment()


def customer_continue():
    """This function runs at the end of the checkout process to allow the user to
    either return to the main menu or quit"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list
    x = str(input("Continue?: y/n\n>>"))

    if x == 'y':
        customer_main()
    elif x == 'n':
        quit()
    else: # recursive if invalid response
        print("Please respond with 'y' or 'n'.")
        customer_continue()


def vendor_int():
    """Runs login or create account for vendor depending on input."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    x = str(input("Are you an existing user?: y/n\n>>"))

    if x == 'y':
        vendor_login()

    elif x == 'n':
        vendor_create_account()

    elif x == 'cancel':
        quit()

    else: # recursive if invalid input
        print("Please respond with 'y' or 'n'.")
        vendor_int()


def vendor_login():
    """Checks input username against vendorname_list and continues to
    displaying vendor options if username is in list"""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    username = str(input("Please enter username:\n>>"))

    if username in vendorname_list:
        user = vendors.Vendor(username)  # instantiates Vendor object if name is in list
        vendor_options()

    elif username == 'cancel':
        quit()

    else:  # returns to int if username not found
        print("Username not found")
        vendor_int()


def vendor_create_account():
    """Creates vendor account and inserts new row into 'vendors' table', then commits change to database.
    Upon successful creation, Vendor object is instantiated and vendor option are displayed."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    username = str(input("Please enter a new username:\n>>"))

    if username in vendorname_list:  # recursive if username already taken
        print("Username already taken.")
        vendor_create_account()

    elif username == 'cancel':
        quit()

    else:
        cur.execute("""INSERT INTO vendors VALUES (?, ?)""",
                    (username, 0))  # 0 value for vendor type as vendors going through sign up will be third party
        con.commit()

        print("User account created.")
        user = vendors.Vendor(username)
        vendor_options()


def vendor_options():
    """Displays commands available to vendors and the calls vendor_main() for input.
    Commands are printed from the options list using tabulate."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    options = [("catalogue", "Show vendor product catalogue."),
               ("orders", "Show all orders"),
               ("add", "Add item to vendor catalogue."),
               ("remove", "Remove item from vendor catalogue."),
               ("order detail", "Show order details."),
               ("order status", "Update the status of an order."),
               ("stock", "Update item stock."),
               ("commands", "Displays commands."),
               ("end", "Save changes and close session."),
               ("cancel", "Cancel transaction. Does not save changes.")]
    print(tabulate(options, headers=["Command", "Description"]))

    vendor_main()


def vendor_main():
    """Executes commands in the options list depending on user input."""

    global item_number, item_list, user, user_basket, user_order, product_list, vendorname_list

    user_input = str(input("Please enter a command:\n>>"))

    if user_input == 'catalogue':  # shows vendor's catalogue using show_catalogue() method
        user.show_catalogue()
        vendor_main()

    elif user_input == 'orders':  # shows all orders using Vendor.show_orders() method
        user.show_orders()
        vendor_main()

    elif user_input == 'add':
        # asks for input for each product detail and then passes them to the Vendor.add_product() method
        name = str(input("Enter product name:\n>>"))
        cost = float(input("Enter product cost:\n>>"))
        stock = int(input("Enter product stock:\n>>"))
        location = str(input("Enter product location:\n>>"))

        user.add_product(name, cost, stock, location)
        vendor_main()

    elif user_input == 'remove':
        prod_id = int(input("Enter Product ID:\n>>"))

        user.remove_product(prod_id)  # input is passed to Vendor.remove_product() method
        vendor_main()

    elif user_input == 'order detail':
        x = int(input("Enter Order ID:\n>>"))
        user.show_order_detail(x)  # shows details of order as specified by input
        vendor_main()

    elif user_input == 'order status':  # updates the order status by passing inputs to Vendor.update_order_state()
        order_id = int(input("Enter Order ID:\n>>"))
        new_state = str(input("Enter new status:\n>>"))

        user.update_order_state(order_id, new_state)
        vendor_main()

    elif user_input == 'stock': # updates product stock by passing inputs to Vendor.update_stock()
        prod_id = int(input("Enter Product ID:\n>>"))
        new_stock = int(input("Enter new stock:\n>>"))

        user.update_stock(prod_id, new_stock)
        vendor_main()

    elif user_input == 'commands':
        vendor_options()

    elif user_input == 'end':  # commits database changes and quits session
        con.commit()
        quit()

    elif user_input == 'cancel': # quits and cancels changes
        quit()

    else:  # recursive if invalid input
        print("Please enter a valid command. Type 'commands' to see a list of available commands.")
        vendor_main()
