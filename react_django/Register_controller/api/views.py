from random import random
from unicodedata import category
from wsgiref.util import request_uri
from django.http import HttpResponse
from django.shortcuts import render
from jinja2 import Undefined
from numpy import empty
from rest_framework import generics, status
from sqlalchemy import null 
from .serializers import Userserializer, createUserSerializer
from .models import USer
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import pandas as pd 
import sqlite3 
connection = sqlite3.connect('db.sqlite3')

# Create your views here. make endpoints 

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
            print(user)
            return Response(json.dumps(user) , status=status.HTTP_200_OK)
        elif category == 'showlist':
            df = pd.read_csv('data.tsv', sep='\t')
            df_copy = df.copy()
            df_copy.drop(['image', 'user_id'], inplace= True, axis = 1)
            print(df_copy)
            user = df_copy.to_json(orient='records')
            print(user)
            return Response(user, status = status.HTTP_200_OK)
        else: 
            return Response({'No request': 'Invalid parameter'}, status= status.HTTP_204_NO_CONTENT)

class CreateUserView(APIView):
    serializer_class = createUserSerializer
    def post(self, request, format = None):
        cursor = sqlite3.connect('db.sqlite3', isolation_level=None, detect_types = sqlite3.PARSE_COLNAMES) 
        print(1)
        print(request.FILES.get('image'))
        print(1)
        '''
        user_id = request.data['user_id']
        if len(user_id) != 6:
            queryset = None
        elif USer.objects.filter(user_id = user_id):
            queryset = USer.objects.filter(user_id = user_id)
            print(queryset[0])
        else:
            queryset = None
        '''     
        
        serializer = self.serializer_class(data = request.data)
        print(serializer)
        if serializer.is_valid(raise_exception= False):
            username = serializer.data.get('username')
            age = serializer.data.get('age')
            print(1)
            if( request.FILES.get('image') == None):
                image_exist = 0
                user = USer(username = username, age = age, Image_flag = image_exist)
                
            else:
                image = request.FILES.get('image')
                image_exist = 1
                user = USer(username = username, age = age, image = image, Image_flag = image_exist)
                    
            user.save()
            db_df = pd.read_sql_query('SELECT * FROM api_user', cursor)
            db_df.to_csv('data.tsv', index= False, sep='\t')
            
            return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)

            ''' # this method - 기존 유저 업데이트는 나중에 생각 
            if(queryset == None):
                user = USer(username = username, age = age, image = image)
                user.save()
                db_df = pd.read_sql_query('SELECT * FROM api_user', cursor)
                db_df.to_csv('data.tsv', index= False, sep='\t')
                return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)
            elif(queryset.exists()):
                user = queryset[0]
                print(user)
                user.age = age
                user.image = image
                user.save(update_fields = ['age', 'image'])
                df = pd.read_csv('data.tsv', index = False ,sep= '\t')
                df.loc[df.iloc[df['user_id'] == user_id], 'age'] = age  
                df.loc[df.iloc[df['user_id'] == user_id], 'image'] = image

                # 이건 파일 저장 잘못된 방법 
                with open('data.txt', 'r', encoding='utf-8') as txtfile: 
                    lines =  txtfile.read()
                    newlist  = re.split(', |\n', lines)
                    id_list = newlist[0::4]
                    newlist[id_list.index(user.user_id)*4+2] = str(user.age)
                    newlist[id_list.index(user.user_id)*4+3] = str(user.image)
                    txtfile.close()
                with open('data.txt', 'w', encoding='utf-8') as txtfile: 
                    pass
                with open('data.txt', 'w', encoding='utf-8') as txtfile: 
                    count = 1
                    for element in newlist:
                        if(count % 4 == 0):
                            txtfile.write(element +'\n')
                        else:
                            txtfile.write(element + ', ')
                        count +=1
                    txtfile.close()'''

        return Response({'Bad Request': 'Invalid data...'}, status= status.HTTP_400_BAD_REQUEST)
