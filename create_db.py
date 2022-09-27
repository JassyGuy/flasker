import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "rmsidrk9!",
)

#print(mydb)

# Create a cursor and initialize it
my_cursor = mydb.cursor()

#Create database
my_cursor.execute("CREATE DATABASE our_users")
#my_cursor.execute("USE our_users")
#my_cursor.execute("CREATE TABLE IF NOT EXISTS our_users (id INT AUTO_INCREMENT PRIMARY KEY, \
#   name VARCHAR(200), \
#  email VARCHAR(120), \
# date_added DATETIME)")

my_cursor.execute("SHOW DATABASES")    
#my_cursor.execute("SELECT * FROM our_users")
for db in my_cursor:
    print(db)
