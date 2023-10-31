from django.contrib.gis.geos import GEOSGeometry
from models import *


# From: https://gis.stackexchange.com/questions/21859/getting-distance-between-2-points-using-geodjango
# Author: ChristopherDBerry
def geo_distance(lat_0, lon_0, lat_1, lon_1):
    point_0 = GEOSGeometry('SRID=4326;POINT({lat} {lon})'.format(lat=lat_0, lon=lon_0))
    point_1 = GEOSGeometry('SRID=4326;POINT({lat} {lon})'.format(lat=lat_1, lon=lon_1))
    return point_0.distance(point_1) * 100

def get_hint(request, guess_lat, guess_lon):
    active_game = ActiveGame.objects.select_related().filter(user=request.user)
    game = active_game.game

    prev_dist = geo_distance(active_game.last_latitude, active_game.last_longitude, game.latitude, game.longitude)
    guess_dist = geo_distance(guess_lat, guess_lon, game.latitude, game.longitude)

