from rest_framework import serializers
from .models import User
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'age', 'image')

class createUserSerializer(serializers.Serializer): # post 다룬다. 
    class Meta:
        model = User 
        fields = ('id','image','age') # post로 받고 싶은것만 -- > 다시 공부해보기 ~!!!!!!!!!!!!!!!!