from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(max_length=40)
    head = models.ImageField(upload_to='profile_images', blank=True)
    gender = models.CharField(max_length=3, blank=True)
    motto = models.CharField(max_length=40, blank=True)


