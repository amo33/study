from django.urls import path
from .views import Userview

urlpatterns = [
    path('home', Userview.as_view()),
    
]