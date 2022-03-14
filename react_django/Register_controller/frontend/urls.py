from .views import index
from django.urls import path 
urlpatterns = [
    path('', index),
    path('list', index),
    path('members', index),
]
