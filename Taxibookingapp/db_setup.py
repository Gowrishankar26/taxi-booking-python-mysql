import pymysql

from vechilemangement.pysql_connection import cursor

con=pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    autocommit=True
)
cursor=con.cursor()
cursor.execute("create database if not exists real_taxi")
cursor.execute("USE real_taxi")
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    password VARCHAR(100)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    lat float,
    lon float,
    is_available boolean default True,
    password VARCHAR(100)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
   customer_id int,
   driver_id int,
   pickup_lat float,
   pickup_lon float,
   drop_lat float,
   drop_lon float,
   distance float,
   fare FLOAT,
   estimated_pickup_time int,
   status varchar(20) default 'Booked',
   booking_time DATETIME,

   FOREIGN KEY (customer_id) REFERENCES customers(id),
   FOREIGN KEY (driver_id) REFERENCES drivers(id)
   
);
""")
cursor.close()
con.close()