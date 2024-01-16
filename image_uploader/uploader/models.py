from django.db import models
import datetime

# Create your models here.
class Images(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images')
    created = models.DateTimeField(default=datetime.datetime.now)