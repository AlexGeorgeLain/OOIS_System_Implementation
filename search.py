import config
#import config module for database connection
from tabulate import tabulate
#import tabulate module for displaying tables

con = config.con
cur = con.cursor()
#sqlite connection and cursor variables


def show_all_products():
    """Collects all products in  catalogue as items in the data list and then prints them using tabulate"""

    data = cur.execute("""SELECT productid, productname, unitcost, stock FROM catalogue""").fetchall()

    print(tabulate(data, headers=["Product ID", "Name", "Cost", "Stock"]))


def search_catalogue(search_term):
    """Collects all products with name that match the search term as items
    in data list, then prints them using tabulate."""

    data = cur.execute("""SELECT productid, productname, unitcost, stock FROM catalogue WHERE productname = ?""",
                       (search_term, )).fetchall()

    print(tabulate(data, headers=["Product ID", "Name", "Cost", "Stock"]))
