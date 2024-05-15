import requests
from geopy.geocoders import Nominatim


def get_location(ip_address):
    # Get location details based on IP address
    geo_request_url = f'https://ipapi.co/{ip_address}/json/'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()

    # Extract latitude and longitude
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    return latitude, longitude


def main():
    ip_address = input("Enter an IP address: ")  # 사용자로부터 IP 주소를 입력받음
    latitude, longitude = get_location(ip_address)
    print(f'Latitude: {latitude}, Longitude: {longitude}')

    # Use geopy to get more detailed location information
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language='en')

    print(location.address)


if __name__ == "__main__":
    main()
