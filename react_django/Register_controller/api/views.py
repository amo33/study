from django.shortcuts import render
from itsdangerous import Serializer
from rest_framework import generics, status 
from .serializers import Userserializer, createUserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here. make endpoints 

class Userview(generics.CreateAPIView):
    qeuryset = User.objects.all()
    serializer_class = Userserializer

class CreateUserView(APIView):
    serializer_class = createUserSerializer
    def post(self, request, format = None):
        pass # tutorial 5 부터 다시 공부! 