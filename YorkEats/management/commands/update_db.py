from django.core.management.base import BaseCommand
import json
from datetime import datetime
from YorkEats.models import *

#Learned commands from https://www.youtube.com/watch?v=GkxpJyuP0Oc

class Command(BaseCommand):
    help = 'Updates database with json data'

    def handle(self, *args, **kwargs):

        Place.objects.all().delete()

        with open("YorkEats/data/dining_dir.json", "r") as json_file:
            data = json.load(json_file)
        for id in data:
            entry = data.get(id)
            if not Place.objects.filter(id=id).exists():
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
                    image_url=entry.get("image_url"),
                    address=entry.get("address")
                    )
                place.save()
            else:
                place = Place.objects.get(id=id)
                place.name = entry.get("location_name")
                place.location_link = entry.get("location")
                place.menu_offering = entry.get("menu_offering")
                place.payment_options = entry.get("payment_options")
                place.menu_href = entry.get("menu").get("menu_href")
                place.dietary_options = entry.get("dietary_options")
                place.opening_days = entry.get("opening_days")
                place.image_url = entry.get("image_url")
                place.address = entry.get("address")
                place.save()
        
        print("Successfully updated the database")