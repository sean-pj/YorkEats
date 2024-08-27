from django.db import models

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

    def __str__(self):
        return f"Name: {self.name}"
    
