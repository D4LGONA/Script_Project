import os
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

LOCATION_API_KEY = os.getenv('LOCATION_API_KEY')

url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
data = {
    'considerIp': True,
}

result = requests.post(url, data)

print(result.text)