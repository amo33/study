from curses.ascii import US
from distutils.command.upload import upload
from email.policy import default
from django.db import models
import uuid
import random
from random import randint 
# Create your models here.


def generate_unique_code():
    length = 6

    while True:
        code = random_with_N_digits(length)
        if USer.objects.filter(user_id = code).count() == 0:
            break

    return str(code)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class USer(models.Model):
    user_id = models.CharField(max_length=50, unique= True, default=generate_unique_code)
    username = models.CharField(max_length=20)
    age = models.IntegerField()
    image = models.ImageField(blank = True, null = True  , upload_to = "images")
    Image_flag = models.IntegerField()
