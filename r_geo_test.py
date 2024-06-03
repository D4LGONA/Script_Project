from geopy.geocoders import Nominatim


def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="qwertyasdfgh")
    location = geolocator.reverse((latitude, longitude), language='ko')

    if location:
        address = location.raw['address']
        province = address.get('province', None)
        city = address.get('city', None)

        if province:
            return province
        else:
            return city
    else:
        return None
