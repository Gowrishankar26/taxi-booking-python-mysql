import pymysql
from datetime import datetime
from utils import calculate_distance
SERVICEABLE_AREAS = [
    "T.Nagar", "Tambaram", "Guindy", "Velachery", "Chrompet",
    "Anna Nagar", "Adyar", "Mylapore", "Egmore", "Saidapet",
    "Kodambakkam", "Nungambakkam", "Pallavaram", "Porur", "Thoraipakkam",
    "Medavakkam", "Perambur", "Ambattur", "Ashok Nagar", "Triplicane"
]



class DBConnection:
    def __init__(self):
        self.con = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='real_taxi'
        )
        self.cursor = self.con.cursor()

    def commit(self):
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()


class BookingSystem(DBConnection):
    def book_ride(self, customer_id):
        print("\n--- Book a Ride ---")
        pickup_place = input("Enter pickup location (e.g., T.Nagar): ")
        drop_place = input("Enter drop location (e.g., Tambaram): ")

        from utils import get_coordinates, calculate_distance, calculate_fare, estimate_pickup_time
        pickup_lat, pickup_lon = get_coordinates(pickup_place)
        drop_lat, drop_lon = get_coordinates(drop_place)

        if pickup_lat is None or drop_lat is None:
            print("Could not fetch coordinates. Please try with a different location.")
            return

        # Find available drivers
        self.cursor.execute("SELECT id, name, lat, lon FROM drivers WHERE is_available=1")
        drivers = self.cursor.fetchall()
        if not drivers:
            print("No drivers available right now.")
            return

        nearest_driver = None
        min_distance = float('inf')

        for driver in drivers:
            driver_id, name, dlat, dlon = driver
            dist = calculate_distance(pickup_lat, pickup_lon, dlat, dlon)
            if dist < min_distance:
                min_distance = dist
                nearest_driver = (driver_id, name, dlat, dlon, dist)

        if nearest_driver:
            driver_id, name, dlat, dlon, pickup_distance = nearest_driver
            total_distance = calculate_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)
            fare = calculate_fare(total_distance)
            estimated_time = estimate_pickup_time(dlat, dlon, pickup_lat, pickup_lon)

            # Save booking
            self.cursor.execute("""
                INSERT INTO bookings (customer_id, driver_id, pickup_lat, pickup_lon,
                    drop_lat, drop_lon, distance, estimated_pickup_time, booking_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                customer_id, driver_id, pickup_lat, pickup_lon, drop_lat,
                drop_lon, total_distance, estimated_time, datetime.now()
            ))

            # Update driver availability
            self.cursor.execute("UPDATE drivers SET is_available=0 WHERE id=%s", (driver_id,))
            self.commit()

            print(f"\n✅ Booking Confirmed with driver {name}")
            print(f"🚕 Fare: ₹{fare}")
            print(f"⏱ Estimated pickup time: {estimated_time} minutes")

    def show_serviceable_areas(self):
        print("\n📍 Our Taxi Service is Available in the Following Areas:\n")
        for i, area in enumerate(SERVICEABLE_AREAS, 1):
            print(f"{i}. {area}")

    def update_booking_status(self):
        print("\n--- Update Booking Status ---")
        booking_id = int(input("Enter booking ID: "))
        new_status = input("Enter new status (Completed/Cancelled): ")
        self.cursor.execute("SELECT driver_id FROM bookings WHERE id=%s", (booking_id,))
        result = self.cursor.fetchone()
        if not result:
            print("Booking not found.")
            return

        driver_id = result[0]
        self.cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (new_status, booking_id))
        self.cursor.execute("UPDATE drivers SET is_available=1 WHERE id=%s", (driver_id,))
        self.commit()
        print("Booking status updated successfully.")

    def view_customer_booking(self, customer_id):
        print("\n--- Active Booking ---")
        self.cursor.execute("""
            SELECT b.id, d.name, b.pickup_lat, b.pickup_lon, b.drop_lat, b.drop_lon,
                   b.status, b.booking_time
            FROM bookings b
            JOIN drivers d ON b.driver_id = d.id
            WHERE b.customer_id=%s AND b.status='Booked'
        """, (customer_id,))
        result = self.cursor.fetchone()
        if result:
            print(f"""
Booking ID: {result[0]}
Driver: {result[1]}
Pickup Location: ({result[2]}, {result[3]})
Drop Location: ({result[4]}, {result[5]})
Status: {result[6]}
Time: {result[7]}
            """)
        else:
            print("No active bookings found.")

    def view_booking_history(self, customer_id):
        print("\n--- Booking History ---")
        self.cursor.execute("""
            SELECT b.id, d.name, b.status, b.booking_time
            FROM bookings b
            JOIN drivers d ON b.driver_id = d.id
            WHERE b.customer_id=%s
            ORDER BY b.booking_time DESC
        """, (customer_id,))
        results = self.cursor.fetchall()
        if not results:
            print("No booking history available.")
            return

        for row in results:
            print(f"ID: {row[0]}, Driver: {row[1]}, Status: {row[2]}, Time: {row[3]}")


