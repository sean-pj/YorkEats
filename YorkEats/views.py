from django.shortcuts import render
from YorkEats.models import *
from django.http import HttpResponse
from datetime import datetime
from YorkEats.models import *

# Create your views here.

def index(request):
    opening_days = Place.objects.first().opening_days

    for day in opening_days:
        opening_days.get(day).replace(" ", "").split("-")

    for place in Place.objects.all():
        open_period = []
        #Many replacements because the dining dir doesnt make their entries consistent please help me
        #https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date
        #https://www.datacamp.com/tutorial/converting-strings-datetime-objects
        for time in place.opening_days.get(datetime.now().strftime('%A')).replace("11 am - 11 pm11 am - 11 pm","11 am - 11 pm").replace(" ", "").replace(".","").replace("&", "-").replace(",", "-").replace("–", "-").replace("to", "-").replace("12", "11:59").split("-"):
            if time == "AllDay":
                place.is_open = True
                place.save()
            elif time == "Closed":
                place.is_open = False
                place.save()
            else:
                try:
                    date_format1 = '%I:%M%p'
                    open_period.append(datetime.strptime(time, date_format1).time())
                except ValueError:
                    date_format1 = '%I%p'
                    open_period.append(datetime.strptime(time, date_format1).time())
        
        #Checks if location is open within the given time periods
        place.is_open = False
        place.save()
        for i in range(0, len(open_period) - 1, 2):
            if open_period[i] <= datetime.now().time() <= open_period[i + 1]:
                place.is_open = True
                place.save()

    return render(request, "yorkeats/index.html", {
        "Places" : Place.objects.all().filter(is_open=True),
        "day_of_week" : datetime.now().strftime('%A')
    })