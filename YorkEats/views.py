from django.shortcuts import render
from YorkEats.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import datetime
from YorkEats.models import *
from django.urls import reverse
from django.db.models.functions import Length
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Update models if place is open
def check_openings(check_time=datetime.now().time(), day_of_week=datetime.now().strftime('%A')):
    # Get opening days
    opening_days = Place.objects.first().opening_days

    for place in Place.objects.all():
        open_period = []

        # Learned datetime from https://docs.python.org/3/library/datetime.html
        # Learned datetime string conversion from https://www.datacamp.com/tutorial/converting-strings-datetime-objects
        # Gets opening times for the current day, splits the opening times into an array with the first element being opening and the second being closed
        for time in place.opening_days.get(day_of_week).replace("11 am - 11 pm11 am - 11 pm","11 am - 11 pm").replace(" ", "").replace(".","").replace("&", "-").replace(",", "-").replace("–", "-").replace("to", "-").replace("12am", "11:59pm").split("-"):
            # Converts text data to datetime objects if possible
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
        
        # Update model if open or closed
        for i in range(0, len(open_period) - 1, 2):
            if open_period[i] <= check_time <= open_period[i + 1]:
                place.is_open = True
                place.save()
            else:
                place.is_open = False
                place.save()

# FUnction for rendering places from index.html, removes some repeated code
def render_places(request, view, title, day_of_week=datetime.now().strftime('%A')):
    if(request.user.is_authenticated):
        ratings = Rating.objects.all().filter(user=request.user)
    else:
        ratings = None

    return render(request, "yorkeats/index.html", {
        "Places" : Place.objects.all().filter(is_open=True),
        "Ratings" :  ratings,
        "day_of_week" : day_of_week,
        # These following options need to be split for each filter
        "locations" : Place.objects.all().order_by("location").values_list('location', flat=True).distinct(),
        # Learned list comprehension to split strings inside a list by whitespace from: https://stackoverflow.com/questions/44085616/how-to-split-strings-inside-a-list-by-whitespace-characters
        "cuisines" : sorted(list(set([element.strip() for elements in Place.objects.all().values_list('menu_offering', flat=True).distinct() for element in elements.split(",")]))),
        # Learned length function from https://docs.djangoproject.com/en/dev/ref/models/database-functions/#length
        "payment_options" : Place.objects.all().order_by(Length('payment_options').desc()).first().payment_options.split(", "),
        "dietary_options" : Place.objects.all().order_by(Length('dietary_options').desc()).first().dietary_options.split(", "),
        # Title and navbar highlight
        "view" : view,
        "title" : title
    })

def index(request):
    check_openings()

    return render_places(request, "open", "Currently Open")

# Updates models with image uploaded from editing a place
@login_required
def edit(request):

    #Must be a post request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get place
    data = request.POST
    place = Place.objects.get(id=int(data.get("id")))

    # Save image to model
    place.image = request.FILES.get("image")
    place.save()
    return JsonResponse(request.POST)

# Updates models with ratings
def rating(request):

    # Must be a post request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # User must be signed in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be logged in to rate."}, status=400)

    # Get star rating from JS
    data = request.POST
    place = Place.objects.get(id=int(data.get("id")))
    stars = int(data.get("stars"))

    # If the user has already rated this place, update that rating, if not create a model
    if len(Rating.objects.filter(user=request.user, place=place)) == 0:
        rating = Rating(place=place, user=request.user, stars=stars)
    else:
        rating = Rating.objects.get(user=request.user, place=place)
        rating.stars = stars
    
    rating.save()
    return JsonResponse({"stars" : place.average_rating()})
            

#Function adapted from previous cs50 projects
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "YorkEats/login.html", {
                "invalid" : "is-invalid",
            })
    else:
        return render(request, "YorkEats/login.html")

#Function adapted from previous cs50 projects
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#Function adapted from previous cs50 projects
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POSt["password"]
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "YorkEats/register.html", {
                "user_invalid" : "is-invalid",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "YorkEats/register.html")

# Returns all post regardless of if it's open
def all(request):

    check_openings()

    if(request.user.is_authenticated):
        ratings = Rating.objects.all().filter(user=request.user)
    else:
        ratings = None

    return render(request, "yorkeats/all.html", {
        "Places" : Place.objects.all(),
        "Ratings" :  ratings,
        "day_of_week" : datetime.now().strftime("%A"),
        # These following options need to be split for each filter
        "locations" : Place.objects.all().order_by("location").values_list('location', flat=True).distinct(),
        # Learned list comprehension to split strings inside a list by whitespace from: https://stackoverflow.com/questions/44085616/how-to-split-strings-inside-a-list-by-whitespace-characters
        "cuisines" : sorted(list(set([element.strip() for elements in Place.objects.all().values_list('menu_offering', flat=True).distinct() for element in elements.split(",")]))),
        # Learned length function from https://docs.djangoproject.com/en/dev/ref/models/database-functions/#length
        "payment_options" : Place.objects.all().order_by(Length('payment_options').desc()).first().payment_options.split(", "),
        "dietary_options" : Place.objects.all().order_by(Length('dietary_options').desc()).first().dietary_options.split(", "),
        # navbar highlight
        "view" : "all"
    })

def later(request):
    if request.method == "POST":

        # convert search_time to datetime object
        try:
            search_time = datetime.strptime(request.POST["datetime"], '%Y-%m-%dT%H:%M')
        except ValueError:
            return render(request, "YorkEats/later.html", {
                "invalid" : "is-invalid"
            })
        day_of_week = search_time.strftime("%A")
        time = search_time.time()
        # Update posts based on whether or not they are open at the searched time
        check_openings(check_time=time, day_of_week=day_of_week)

        return render_places(request, "later", "Open at: " + search_time.strftime('%Y-%m-%d %H:%M %p'), day_of_week=day_of_week)
    else:
        return render(request, "YorkEats/later.html")
        