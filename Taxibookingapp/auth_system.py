import pymysql
import re

from django.db.models.expressions import result

from utils import get_coordinates
class DBConnection:
    def __init__(self):
        self.con=pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='real_taxi',
        )
        self.cursor=self.con.cursor()
    def commit(self):
        self.con.commit()
    def close(self):
        self.cursor.close()
        self.con.close()
class AuthSystem(DBConnection):
    def is_valid_phone(self,number):
        if len(number) !=10 or not number.isdigit():
            return False
        if number[0]  not in ['6','7','8','9']:
            return False
        return True
    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        return re.match(pattern, email) is not None

    def register_customer(self):
        name=input("Enter Customer name:")
        while True:
            phone=input("Enter phone:")
            if self.is_valid_phone(phone):
                break
            else:
                print(" Invalid phone number. Must be 10 digits and start with 6, 7, 8, or 9.")
        while True:
            email=input("Enter Email:")
            if self.is_valid_email(email):
                break
            else:
                print("Invalid email format.Must contain '@' and domain like .com" )
        password=input("Enter password:")
        self.cursor.execute("""Insert into customers(name,phone,email,password)values(%s,%s,%s,%s)""",(name,phone,email,password))
        self.commit()
        print("Customer registered successfully!")
    def login(self):
        phone=input("Enter phone:")
        password=input("Enter Password:")

        self.cursor.execute("""select id,name from customers where phone=%s and password=%s""",(phone,password))
        result=self.cursor.fetchone()
        if result:
            print(f"Welcome {result[1]}! your customer Id is {result[0]}")
            return result[0]
        else:
            print("Invalid Credentials")
            return  None
    def register_driver(self):
        name=input("Enter Driver Name: ")

        while True:
            phone=input("Enter phone Number:")
            if self.is_valid_phone(phone):
                break
            else:
                print(" Invalid phone number. Must be 10 digits and start with 6, 7, 8, or 9.")

        password=input("Enter password")
        location=input("Enter your current location(e.g,T.Nagar): ")
        lat,lon=get_coordinates(location)
        if lat is None or lon is None:
            print("Could not find the Location. Try again.")
            return
        self.cursor.execute("""insert into drivers(name,phone,lat,lon,password)values(%s,%s,%s,%s,%s)""",(name,phone,lat,lon,password))
        self.commit()
        print(f"Driver registered sucessfully at{lat:.4f},{lon:.4f}")
    def login_driver(self):
        phone=input("Enter phone number:")
        password=input("Enter password:")
        self.cursor.execute("""select id ,name from drivers where phone=%s and password=%s""",(phone,password))
        result=self.cursor.fetchone()
        if result:
            print(f"Welcome {result[1]} "
                  f""
                  f"(Driver Id:{result[0]})")
            return result[0]
        else:
            print("Invalid Crentials")
            return None
if __name__=="__main__":
    app=AuthSystem()
    while True:
        print("1.Register Customer.")
        print("2.Login Customer.")
        print("3.Register Driver")
        print("4.Login Driver.")
        print("5.Exit.")
        ch=input("Enter your choice:")
        if ch=="1":
            app.register_customer()
        elif ch=='2':
            app.login()
        elif ch=='3':
            app.register_driver()
        elif ch=='4':
            app.login_driver()
        elif ch=='5':
            print("Thank you! Bye")
            app.close()
            break
        else:
            print("Invalid option.Try Again.")