from rest_framework import serializers
from .models import USer
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = USer
        fields = ('user_id','username', 'age', 'Image_flag')

class createUserSerializer(serializers.ModelSerializer): # post 다룬다. 
    image = serializers.ImageField( allow_null = True) 
    class Meta:
        model = USer 
        fields = ('username','age','image') # post로 받고
        