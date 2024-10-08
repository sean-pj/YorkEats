from django.db import models
from django.contrib.auth.models import AbstractUser
import urllib.request
import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class User(AbstractUser):
    pass

# Model for each restaurant
class Place(models.Model):
    name = models.TextField()
    location = models.TextField()
    location_link = models.TextField()
    menu_offering = models.TextField()
    payment_options = models.TextField()
    menu_name = models.TextField()
    menu_href = models.TextField()
    dietary_options = models.TextField()
    opening_days = models.JSONField(null=True, blank=True)
    is_open = models.BooleanField(default=False)
    # auto_now updates every time the instance is saved, auto_now_add updates only on creation
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    address = models.TextField(default="No address found", null=True)

    # Learned average rating function from https://www.reddit.com/r/djangolearning/comments/1b9jfit/how_to_properly_setup_rating_stars/
    # Return a float representing the average rating
    def average_rating(self):
        if self.ratings != None:
            ratings = self.ratings.all()
            if ratings.aggregate(models.Avg('stars'))['stars__avg'] != None:
                return ratings.aggregate(models.Avg('stars'))['stars__avg']
            else:
                return 0
        else: 
            return 0 
    
    # Rounds average rating
    def round_average_rating(self):
        return round(self.average_rating())

    # Saves an image from using a passed image url
    def save_image(self, url):
        result = urllib.request.urlretrieve(url)
        temp_image = NamedTemporaryFile()
        temp_image.write(open(result[0], 'rb').read())
        temp_image.flush()
        self.image.save(f"{self.id} : {self.name}.jpg", File(temp_image))
        self.save()
        
    def __str__(self):
        return f"Name: {self.name}"

# 5 Star rating model
class Rating(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    stars = models.IntegerField(default=1)

    
