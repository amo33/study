from dataclasses import replace
from random import random
from django.shortcuts import redirect
from rest_framework import generics, status
from sqlalchemy import true
from .serializers import Userserializer, createUserSerializer
from .models import USer
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from pathlib import Path
import pandas as pd 
import sqlite3 
from PIL import Image
connection = sqlite3.connect('db.sqlite3')

# Create your views here. make endpoints 
class SpecificView(generics.CreateAPIView):
    serializer_class = Userserializer
    def get(self, request, format = None):
        method = request.GET.get('method', None)
        id = request.GET.get('user_id',None)
        
        user = []
        if method == 'showdb':
            queryset = USer.objects.filter(id=id)

            user.append({
                "user_id" : queryset[0].user_id,
                "username": queryset[0].username,
                "age" : queryset[0].age,
                "image_path" : queryset[0].image_path, 
            })
        elif method == 'showlist':
            df = pd.read_csv('data.tsv', sep='\t')
            df_copy = df.copy()
            df_copy.fillna('0', inplace=True)
            user.append({
                "user_id" : df_copy.iloc[int(id)-1]['user_id'],
                "username": df_copy.iloc[int(id)-1]['username'],
                "age":df_copy.iloc[int(id)-1]['age'],
                "image_path":df_copy.iloc[int(id)-1]['image_path'],
            })
           
        return Response( user, status = status.HTTP_200_OK)

class Userview(generics.CreateAPIView):
    serializer_class = Userserializer
    def get(self, request, format= None): # list와 데이터베이스가 get방식으로 들어오면 그걸로 query 찾는다.
        category = request.GET.get('category', None)
        if category == 'showdb':
            qeuryset = USer.objects.all()
            user = []
            for element in qeuryset:
                user.append({
                    "id" : element.id,
                    "username": element.username,
                    "age": element.age,
                    "Image_flag" : element.Image_flag
                })
           
            return Response(user , status=status.HTTP_200_OK)
        elif category == 'showlist':
            df = pd.read_csv('data.tsv', sep='\t')
            df_copy = df.copy()
           
            df_copy.fillna('0', inplace=True)
            user = df_copy.to_dict('records')
            
            return Response(user, status = status.HTTP_200_OK)
        else: 
            return Response({'No request': 'Invalid parameter'}, status= status.HTTP_204_NO_CONTENT)

class CreateUserView(APIView):
    serializer_class = createUserSerializer
    def post(self, request, format = None):
        cursor = sqlite3.connect('db.sqlite3', isolation_level=None, detect_types = sqlite3.PARSE_COLNAMES) 
        
        serializer = self.serializer_class(data = request.data)

 
        if serializer.is_valid():
            
            username = serializer.data.get('username')
            age = serializer.data.get('age')
            
           
            image = request.FILES.get('image')
            image_for_thumb = Image.open(image)
            size = (128, 128)
            image_for_thumb.thumbnail(size)
            image_path = "/thumbnailed/"+str(image)
            image_for_thumb.save(Path('user_register/public'+image_path))
            
            image_exist = 1
            user = USer(username = username, age = age, image = image, image_path = image_path, Image_flag = image_exist)
                    
            user.save()
            db_df = pd.read_sql_query('SELECT * FROM api_user', cursor)
            db_df.to_csv('data.tsv', index= False, sep='\t')
            
            return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)
        elif (request.FILES.get('image') == None): 

            username = serializer.data.get('username')
            age = serializer.data.get('age')
            image_exist = 0
            user = USer(username = username, age = age, Image_flag = image_exist, image_path = ' ')
            
            user.save()
            db_df = pd.read_sql_query('SELECT * FROM api_user', cursor)
            db_df.to_csv('data.tsv', index= False, sep='\t')
            
            return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status= status.HTTP_400_BAD_REQUEST)
