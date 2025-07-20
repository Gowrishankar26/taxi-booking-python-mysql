from auth_system import AuthSystem
from booking_system import BookingSystem

def main():
    print("==== Welcome to Real Taxi Booking System ====")
    auth = AuthSystem()
    booking = BookingSystem()

    while True:
        print("\n1. Register as Customer")
        print("2. Login as Customer")
        print("3. Register as Driver")
        print("4. Login as Driver")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            auth.register_customer()
        elif choice == '2':
            customer_id = auth.login()
            if customer_id:
                while True:
                    print("1. Book a Ride")
                    print("2. View My Current Booking")
                    print("3. View My Booking History")
                    print("4. Show Serviceable Areas")  # ✅ NEW
                    print("5. Logout")

                    sub_choice = input("Enter your choice: ")

                    if sub_choice == '1':
                        booking.book_ride(customer_id)
                    elif sub_choice == '2':
                        booking.view_customer_booking(customer_id)
                    elif sub_choice == '3':
                        booking.view_booking_history(customer_id)
                    elif sub_choice =='4':
                        booking.show_serviceable_areas()

                    elif sub_choice == '5':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            auth.register_driver()
        elif choice == '4':
            driver_id = auth.login_driver()
            if driver_id:
                while True:
                    print("\n---- Driver Menu ----")
                    print("1. Update Booking Status")
                    print("2. Logout")

                    driver_choice = input("Enter your choice: ")

                    if driver_choice == '1':
                        booking.update_booking_status()
                    elif driver_choice == '2':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '5':
            print("Thank you for using the Real Taxi Booking System.")
            auth.close()
            booking.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
