from curses.ascii import US
from distutils.command.upload import upload
from django.db import models
import uuid
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

class USer(models.Model):
    user_id = models.CharField(max_length=50, unique= True, default=uuid.uuid1)
    username = models.CharField(max_length=20)
    age = models.IntegerField()
    image = models.ImageField(blank = True, null = True, upload_to = "images")
