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
            place = Place(
                name=entry.get("location_name"),
                location=entry.get("location"), 
                location_link=entry.get("location_link"), 
                menu_offering=entry.get("menu_offering"),
                payment_options=entry.get("payment_options"),
                menu_name=entry.get("menu").get("menu_name"),
                menu_href=entry.get("menu").get("menu_href"),
                dietary_options=entry.get("dietary_options"),
                opening_days=entry.get("opening_days")
                )
            place.save()
        
        print("Successfully updated the database")
        
        
        # period = []
        # week_day = []
        # for day in data.get("Pizza Studio").get("opening_days"):
        #     week_day.append(day)
        #     period.append(data.get("Pizza Studio").get("opening_days").get(day).replace(" ", "").split("-"))
        # week_day.append(week_day.pop(0))
        # print(week_day)
        # print(period)
        # for range in period:
        #     for time in range:
        #         try:
        #             date_format1 = '%I:%M%p'
        #             print(datetime.strptime(time, date_format1).time())
        #         except ValueError:
        #             date_format1 = '%I%p'
        #             print(datetime.strptime(time, date_format1).time())


        # https://www.datacamp.com/tutorial/converting-strings-datetime-objects
        # date_str = '02/28/2023 02:30 PM'
        # date_format = '%m/%d/%Y %I:%M %p'
        # date_str1 = '02:30 PM'
        # date_format1 = '%I:%M %p'
        # date_str2 = '02:30 PM'
        # date_format2 = '%I:%M %p'

        # date_obj1 = datetime.strptime(date_str1, date_format1)
        # date_obj2 = datetime.strptime(date_str2, date_format2)
        # print(date_obj2)
        # print(date_obj1 == date_obj2)