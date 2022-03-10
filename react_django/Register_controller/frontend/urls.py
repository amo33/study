from .views import index
from django.urls import path 
urlpatterns = [
    path('', index),
    path('GotoList', index),
    path('showlist', index),
    path('showdb', index),
    path('register', index),
]
