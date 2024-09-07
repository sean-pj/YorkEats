from django.core.management.base import BaseCommand
import requests
import json

GOOGLE_API_KEY = ''

#https://developers.google.com/maps/documentation/places/web-service/search-text
#https://developers.google.com/maps/documentation/places/web-service/place-photos
def get_place_data(name, building):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': f'{name}, {building}, York University',
        'inputtype': 'textquery',
        'fields': 'formatted_address,photos',
        'key': GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        # Get the first photo reference
        if 'photos' in data['candidates'][0]:
            photo_reference = data['candidates'][0]['photos'][0]['photo_reference']
            # Use the photo reference to get the image URL
            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxheight=140&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
        else:
            image_url = "#"
        
        if 'formatted_address' in data['candidates'][0]:
            address = data['candidates'][0]['formatted_address']
        else:
            address = "No address found"

        # return image_url + address
        return address, image_url
        
    else:
        return None

class Command(BaseCommand): 
    help = 'Updates dining directory json data with images and address found from the google maps API'
    def handle(self, *args, **kwargs):

        try:
            with open("YorkEats/config/keys.json", "r") as json_file:
                data = json.load(json_file)
                GOOGLE_API_KEY = data.get("Google")
                print(GOOGLE_API_KEY)
        except FileNotFoundError:
            return "No API key found. Please add a Google API key to the config/keys.json file"

        # address, image_url = get_place_data("Yogen Fruz", "First Student Center")
        # print(address)
        # print(image_url)

        with open("YorkEats/data/dining_dir.json", "r") as json_file:
            data = json.load(json_file)

        for i in data:
            place = data.get(i)
            if (get_place_data(place.get("location_name"), place.get("location")) != None):
                address, image_url = get_place_data(place.get("location_name"), place.get("location"))
                place.update({
                    "address" : address,
                    "image_url" : image_url
                })

        #https://www.javatpoint.com/save-json-file-in-python
        #convert dictionary to json file
        dining_dir = open("YorkEats/data/dining_dir.json", "w")
        json.dump(data, dining_dir, indent=4)
        dining_dir.close()

        print("Updated json data with google maps info successfully, use the update_db command to update the django models")