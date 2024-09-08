from django.core.management.base import BaseCommand
import requests
import json
from YorkEats.models import *

# Learned to use google API from the following documentation:
# https://developers.google.com/maps/documentation/places/web-service/search-text
# https://developers.google.com/maps/documentation/places/web-service/place-photos

# Gets address and photo url from google places API
def get_place_data(name, building, GOOGLE_API_KEY):
    # Search text url
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    # JSON parameters for API request
    params = {
        'input': f'{name}, {building}, York University',
        'inputtype': 'textquery',
        'fields': 'formatted_address,photos',
        'key': GOOGLE_API_KEY
    }
    # Send request to API, response is returned as JSON
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        # Get the first photo reference
        if 'photos' in data['candidates'][0]:
            photo_reference = data['candidates'][0]['photos'][0]['photo_reference']
            # Use the photo reference to get the image URL
            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
        else:
            image_url = "#"
        
        # Get the formatted address
        if 'formatted_address' in data['candidates'][0]:
            address = data['candidates'][0]['formatted_address']
        else:
            address = "No address found"

        # return image_url + address
        return address, image_url
        
    else:
        return None

# Learned commands from https://www.youtube.com/watch?v=GkxpJyuP0Oc
class Command(BaseCommand): 
    help = 'Updates models with images and addresses from Google\'s Places API. JSON data is updated with addresses.'

    def handle(self, *args, **kwargs):

        # Get API key from config file
        try:
            with open("YorkEats/config/keys.json", "r") as json_file:
                data = json.load(json_file)
                GOOGLE_API_KEY = data.get("Google")
        except FileNotFoundError:
            return "No config file found. Please add YorkEats/config/keys.json file with the Google API key."
        
        # Open JSON data
        with open("YorkEats/data/dining_dir.json", "r") as json_file:
            data = json.load(json_file)

        for i in data:
            # Get place from JSON data
            place_json = data.get(i)

            # Use JSON data to make requests to google api
            if get_place_data(place_json.get("location_name"), place_json.get("location"), GOOGLE_API_KEY) != None:
                address, image_url = get_place_data(place_json.get("location_name"), place_json.get("location"), GOOGLE_API_KEY)
                #Update JSON data with address
                place_json.update({
                    "address" : address,
                })
            else:
                return "API key is invalid or not returning data"
            
            # Update models with images from API
            if (image_url != "#"):
                place = Place.objects.get(id=(int(i) +1))
                place.save_image(image_url)
                place.address = address
                place.save()

        # Learned to save JSON from https://www.javatpoint.com/save-json-file-in-python
        # Update JSON data
        dining_dir = open("YorkEats/data/dining_dir.json", "w")
        json.dump(data, dining_dir, indent=4)
        dining_dir.close()

        print("Updated json data and models with google maps info successfully.")