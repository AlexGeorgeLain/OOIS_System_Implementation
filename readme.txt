Requirements and Running:

This code requires the third party tabulate module to run. I have amended the “Run” config in Codio to install the this
module before executing my code. Alternatively, and for testing in the command line, use the command

	python3 -m pip install tabulate

to install tabulate before executing this code.

Main.py runs the code on the main database.db and commits permanent changes when appropriate based on the user input.

Test.py will generate and in-memory database which is structured in the same way and contains some of the same dummy
data, but all changes are lost when the programme is quit.


———


Testing:

Their are four test files (test1.txt, test2.txt, test3.txt, test4.txt) provided which can be used along with test.py to
input a series of commands and quit. This can be run in the command line using the

	cat <filename>.txt | python3 test.py

command.

Test1.txt will login in as the returning customer “testuser”, display the entire product catalogue, search the catalogue
for “apple”, and add items to the basket and display the basket contents. An item will then be removed from the
basket, and the basket is displayed again to show the change. The user then proceeds through the checkout process, using
and saving a new address, choosing the delivery method, and using and saving a new payment method. The user then
continues shopping and then inputs “cancel” to quit. This test uses every step in customer order process and finishes
successfully.

Test2.txt will simply create a new customer user account and exit. After the new account is created the remaining order
process is the same as that of a new user, so there is no need for the test to run past that point. This test also runs
successfully.

Test3.txt will login as the vendor “vendor123”, and display the vendor’s product catalogue. The vendor will then add and
remove a product from the catalogue, displaying the catalogue after both process to show the changes. Next the stock of
a product is update and the catalogue is shown to reflect the changes. A list of all orders is then displayed, and the
details of a specific order are then show. This order’s status is then updated. Finally the vendor views all available
commands and ends their session. This test uses every function available to the vendors and completes successfully.

Test4.txt will simply create a new vendor account and add a product to their catalogue. This completes successfully.

When the test.py file is run, an in-memory database is created so that any errors are none destructive. The customer
accounts that are already available are “testuser” and “user123”. The vendor accounts available are “firstpartyvendor”
and “vendor123”.


———


Solution Description:

This solution is somewhat simpler than my initial UML class diagram. I chose to validate users simply based on their
username which I found meant that there was no need for the parent/child class relationship shown in my previously
submitted diagram. If a username/password login system was implemented in the future then this could changed with
relative ease.

he second change I made when doing this implementation was to remove the “Product” object. Instead I have chosen to
have a “catalogue” table in the database which a Vendor object can update product information in directly, and from
which information can be read directly from when instantiating a BasketItem object. the BasketItem, Basket, Customer
relationship remains the same.

I have opted to remove the Address and PaymentMethod classes from this initial implementation, and instead store the
saved preferences as attributes in the Customer class. This also means that the update methods for each are now in the
Customer class methods.

Instead creating an OrderDetail class and creating a new instance of it each for BasketItem object held in the Basket
contents attribute, I have chosen to instead pass the Customer and Basket item into the Order object. This allows for
the original BasketItem instances to be maintained until the payment is completed, and the order details are saved in
the database.


———


Further Improvements:

The use of a third party package is not ideal. If this implementation were to move forward, I would ideally look to
find a combination of built-in Python packages to achieve a satisfactory result for print tables, or develop my own
module to replicate the results given by the tabulate package. Given the time constraints on the assignment, I decided
that it was more beneficial to use a proven third party solution to deliver a working proof of concept.

For this implementation I have written my own interface. However, this means the code is may become hard to update and
maintain if additional functionality required. The interface.py module could be simplified in the future by using a
built-in Python package such as argparse.

The database structure could also be improved slightly. Currently the ‘catalogue’ is one table and displays only the
relevant products to each vendor using the system. This could become unwieldy over time if the platform was used by
enough vendors selling enough products. An alternative would be the create a new table for each vendor when they create
an account which holds only their catalogue. This would be fairly straight forward to implement. The “orderitems” table
could be broken up in a similar way if necessary. Another useful addition which could be made would be to add a ‘tags’
column to the ‘catalogue’ table. The search function currently searches the ‘productname’ column, and only returns exact
matches. Tags would allow for more general searches such as “fruit” instead of “apple”.