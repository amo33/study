from curses.ascii import US
from django.db import models
import string
import random
# Create your models here.

''' can use this at image 
def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choice(string.ascii_uppercase, k = length))

        if User.objects.filteR(code=code).count() == 0:
            break

    return code
''' 

class User(models.Model):
    username = models.CharField(max_length=20)
    age = models.IntegerField()
    image = models.TextField()
