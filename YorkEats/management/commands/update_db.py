from django.core.management.base import BaseCommand
import json
from datetime import datetime
from YorkEats.models import *

# Learned commands from https://www.youtube.com/watch?v=GkxpJyuP0Oc

class Command(BaseCommand):
    help = 'Updates database with json data'

    def handle(self, *args, **kwargs):

        # Get JSON data from file
        with open("YorkEats/data/dining_dir.json", "r") as json_file:
            data = json.load(json_file)
        
        # For every place in data update or create a Place model
        for id in data:
            entry = data.get(id)
            if not Place.objects.filter(id=(int(id) + 1)).exists():
                place = Place(
                    name=entry.get("location_name"),
                    location=entry.get("location"), 
                    location_link=entry.get("location_link"), 
                    menu_offering=entry.get("menu_offering"),
                    payment_options=entry.get("payment_options"),
                    menu_name=entry.get("menu").get("menu_name"),
                    menu_href=entry.get("menu").get("menu_href"),
                    dietary_options=entry.get("dietary_options"),
                    opening_days=entry.get("opening_days"),
                    address=entry.get("address")
                    )
                place.save()
            else:
                place = Place.objects.get(id=(int(id) + 1))
                place.name = entry.get("location_name")
                place.location_link = entry.get("location")
                place.menu_offering = entry.get("menu_offering")
                place.payment_options = entry.get("payment_options")
                place.menu_href = entry.get("menu").get("menu_href")
                place.dietary_options = entry.get("dietary_options")
                place.opening_days = entry.get("opening_days")
                place.address = entry.get("address")
                place.save()
        
        print("Successfully updated the database")