from rest_framework import generics, status
from .serializers import Userserializer, createUserSerializer
from .models import USer
from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
import pandas as pd 
import uuid
from PIL import Image
import os 

class Userview(generics.CreateAPIView, APIView):  
    serializer_class = createUserSerializer
    def post(self, request, format = None): 
        serializer = self.serializer_class(data = request.data)
        if os.stat("data.tsv").st_size == 0:
            f = open("data.tsv", "a")
            line =['{}\t{}\t{}\t{}\t{}\n'.format('id', 'user_id','username','age','image_path')]
            f.writelines(line)
            f.close()
        if serializer.is_valid():
            
            username = serializer.data.get('username')
            age = serializer.data.get('age')
            if request.FILES.get('image')!= None:
                image = request.FILES.get('image')
                image_for_thumb = Image.open(image) 
                size = (128, 128)
                image_for_thumb.thumbnail(size)
                image_path = "/thumbnailed/"+str(uuid.uuid4())+str(image)
                image_for_thumb.save(Path('user_register/public'+image_path))
            else:
                image_path = None
            user = USer(username = username, age = age, image_path = image_path)
            
            user.save()
            f = open("data.tsv", "a") #저장
            userline=['{}\t{}\t{}\t{}\t{}\n'.format(user.id,user.user_id,user.username,user.age,user.image_path)]
            f.writelines(userline)
            f.close()
            
            return Response(Userserializer(user).data, status= status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status= status.HTTP_400_BAD_REQUEST)
    serializer_class = Userserializer
    def get(self, request, format= None): 
        method = request.GET.get('method', None)
        id = request.GET.get('user_id',None)
        
        if method == 'showdb':
            queryset = USer.objects.all() if id == None else USer.objects.filter(id=id)
            user = []
            for element in queryset:
                user.append({
                    "id" : element.id,
                    "username": element.username,
                    "age": element.age,
                    "Image_flag" : 1 if element.image_path != None else 0,
                    "image_path" : element.image_path if id != None else None,
                })
            
            return Response(user , status=status.HTTP_200_OK)
        elif method == 'showlist':
            df = pd.read_csv('data.tsv', sep='\t')
            print(df)
            df_copy = df.copy()
            
            df_copy['Image_flag'] = df_copy['image_path'].apply(lambda x :1 if x != 'None' else 0)
            if id == None:
                df_copy.drop('image_path', axis=1, inplace=True)
                user = df_copy.to_dict('records')
            elif id != None:
                print(id)
                print(type(id))
                print(type(df_copy['id']))
                user = []
                idx =df_copy.index[df_copy['id'].equals(id)].tolist()
                print(idx)
                user.append({
                     "user_id" : df_copy[idx, 'user_id'],
                     "username": df_copy[idx, 'username'],
                     "age":df_copy[idx, 'age'],
                     "image_path":df_copy[idx , 'image_path'],
                 })
            return Response(user, status = status.HTTP_200_OK)
        else: 
            return Response({'No request': 'Invalid parameter'}, status= status.HTTP_204_NO_CONTENT)
 