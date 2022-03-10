from rest_framework import serializers
from .models import USer
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = USer
        fields = ('user_id','username', 'age', 'image')

class createUserSerializer(serializers.HyperlinkedModelSerializer,serializers.ModelSerializer): # post 다룬다. 
    class Meta:
        model = USer 
        fields = ('username','age', 'image') # post로 받고 