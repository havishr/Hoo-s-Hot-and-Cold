import json

from models import *

API_KEY = "AIzaSyDY4E9uAdgpAZNzSTNIofmkZdKAAIE37X4"


# Create a Google Maps distance query request
def distance_request(origin_lat, origin_lon, dest_lat, dest_lon):
    return """
    https://maps.googleapis.com/maps/api/distancematrix/json
        ?destinations={dest_lat}%2C{dest_lon}
        &origins={origin_lat}%2C{origin_lon}
        &mode=walking
        &key={api_key}
    """.format(dest_lat=dest_lat, dest_lon=dest_lon,
               origin_lat=origin_lat, origin_lon=origin_lon,
               api_key=API_KEY)


# Get distance value form JSON request
def distance_from_response(response):
    data = json.loads(response)
    value = data['rows'][0]['elements'][0]['distance']['value']
    return value


# Check if player has moved towards or away from the destination
def hint(prev_lat, prev_lon, curr_lat, curr_lon, game):
    prev_dist = distance_from_response(
        distance_request(prev_lat, prev_lon, game.latitude, game.longitude)
    )
    new_dist = distance_from_response(
        distance_request(curr_lat, curr_lon, game.latitude, game.longitude)
    )
    if new_dist < prev_dist:
        return "HOT"
    return "COLD"
