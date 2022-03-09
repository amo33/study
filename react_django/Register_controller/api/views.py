from django.shortcuts import render
from rest_framework import generics, status 
from .serializers import Userserializer, createUserSerializer
from .models import USer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here. make endpoints 

class Userview(generics.CreateAPIView):
    qeuryset = USer.objects.all()
    serializer_class = Userserializer

class CreateUserView(APIView):
    serializer_class = createUserSerializer
    def post(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            age = serializer.data.get('age')
            image = serializer.data.get('image')
            user_id= self.request.session.session_key
            queryset = USer.objects.filter(user_id = user_id)

            if(queryset.exists()):
                user = queryset[0]
                user.age = age
                user.image = image
                user.save(update_fields = ['age', 'image'])

                return Response(Userserializer(user).data, status= status.HTTP_200_OK)
            else:
                user = USer(username = username, age = age, image = image)
                user.save()

                return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)
        
        return Response({'Bad Request': 'Invalid data...'}, status= status.HTTP_400_BAD_REQUEST)
