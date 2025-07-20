import requests
import math

def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place},Chennai&format=json"
    headers = {"User-Agent": "TaxiBookingApp"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None
def calculate_distance(lat1,lon1,lat2,lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance=R * c
    return round(distance,2)
def calculate_fare(distance_km):
    base_fare=40
    per_km_rate=12
    fare = base_fare + (distance_km * per_km_rate)

    return round(fare,2)
def estimate_pickup_time(driver_lat,driver_lon,pickup_lat,pickup_lon):
    distance=calculate_distance(driver_lat,driver_lon,pickup_lat,pickup_lon)
    average_speed_kmph=30
    time_minutes=(distance/average_speed_kmph)*60
    return int(time_minutes)


