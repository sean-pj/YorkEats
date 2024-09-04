from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# Create your models here.
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
    #auto_now updates every time the instance is saved, auto_now_add updates only on creation
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    # https://www.reddit.com/r/djangolearning/comments/1b9jfit/how_to_properly_setup_rating_stars/
    def average_rating(self):
        if self.ratings != None:
            ratings = self.ratings.all()
            if ratings.aggregate(models.Avg('stars'))['stars__avg'] != None:
                return ratings.aggregate(models.Avg('stars'))['stars__avg']
            else:
                return 0
        else: 
            return 0 

    def __str__(self):
        return f"Name: {self.name}"
    
class Rating(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    stars = models.IntegerField(default=1)

    
