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

    def __str__(self):
        return f"Name: {self.name}"

    
