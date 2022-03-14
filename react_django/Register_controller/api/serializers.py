from rest_framework import serializers
from .models import USer
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = USer
        fields = ('user_id','username', 'age', 'image','Image_flag')

class createUserSerializer(serializers.ModelSerializer): # post 다룬다. 
    # image = serializers.ImageField( allow_empty_file = True, required = False, max_length = None) 
    class Meta:
        model = USer 
        fields = ('username','age','image') # post로 받고
        