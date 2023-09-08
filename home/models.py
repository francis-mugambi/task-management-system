from django.db import models
import random
import string
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):   
    first_name = models.CharField(max_length=70, blank=True);
    middle_name = models.CharField(max_length=70, blank=True);
    last_name = models.CharField(max_length=70, blank=True);
    email = models.CharField(max_length=70, blank=True);
    phone = models.CharField(max_length=20);
    id_number = models.CharField(max_length=10);
    USER_NAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Task(models.Model):   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100);
    description = models.CharField(max_length=200);
    status = models.CharField(max_length=200);
    due_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.owner.email
