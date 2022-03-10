from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status 
from .serializers import Userserializer, createUserSerializer
from .models import USer
from rest_framework.views import APIView
from rest_framework.response import Response
import re 
# Create your views here. make endpoints 

class Userview(generics.CreateAPIView):
    serializer_class = Userserializer
    def get(self, request, format= None): # list와 데이터베이스가 get방식으로 들어오면 그걸로 query 찾는다.
        category = request.GET.get('category', None)
        if category == 'showdb':
            qeuryset = USer.objects.all()
            user = qeuryset[1]
            return Response(Userserializer(user).data)
        elif category == 'showlist':
            with open('data.txt', 'r', encoding='utf-8') as txtfile: 
                lines =  txtfile.read()
            txtfile.close()
            return HttpResponse(lines, content_type='text/plain')
        else: 
            return Response({'No request': 'Invalid parameter'}, status= status.HTTP_204_NO_CONTENT)

class CreateUserView(APIView):
    serializer_class = createUserSerializer
    def post(self, request, format = None):
        file_obj = request.FILES['image'] # files들을 따로 찾아서 넣어줘야한다.
        if USer.objects.filter(image = file_obj):
            user_id = USer.objects.filter(image = file_obj)[0].user_id
        else:
            self.request.session.create()
        
        serializer = self.serializer_class(data = request.data)
        print(1)
        if serializer.is_valid():
            username = serializer.data.get('username')
            age = serializer.data.get('age')
            image = file_obj
            user_id= self.request.session.session_key
            print(1)
            queryset = USer.objects.filter(user_id = user_id)
            
            if(queryset.exists()):
                user = queryset[0]
                print(user)
                user.age = age
                user.image = image
                user.save(update_fields = ['age', 'image'])
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
                    txtfile.close()
                return Response(Userserializer(user).data, status= status.HTTP_200_OK)
            else:
                user = USer(user_id = user_id, username = username, age = age, image = image)
                user.save()
                with open('data.txt', 'w', encoding='utf-8') as txtfile:
                    line = [str(user_id), ', ', username, ', ',str(age), ', ', str(image), '\n']
                    print(line)
                    txtfile.writelines(line)
                    txtfile.close()
                print(1)
                return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)
        
        return Response({'Bad Request': 'Invalid data...'}, status= status.HTTP_400_BAD_REQUEST)
