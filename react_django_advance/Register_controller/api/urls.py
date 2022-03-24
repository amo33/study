from curses.ascii import SP
from django.urls import path
from .views import Userview

urlpatterns = [
    path('home', Userview.as_view()),
    path('create-user', Userview.as_view()),
    path('List',Userview.as_view()),
    path('detail', Userview.as_view())
]
