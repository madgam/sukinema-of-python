# Google API モジュール
from pygeocoder import Geocoder
import googlemaps
import os


class Geocoder():

    @classmethod
    def getLatlong(cls, location):
        googleapikey = os.environ['GOOGLE_GEOCODING_API_KEY']
        gmaps = googlemaps.Client(key=googleapikey)
        result = gmaps.geocode(location)

        latlong = {}
        latlong['latitude'] = result[0]['geometry']['location']['lat']
        latlong['longitude'] = result[0]['geometry']['location']['lng']

        return latlong
