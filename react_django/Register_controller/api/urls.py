from curses.ascii import SP
from django.urls import path
from .views import SpecificView, Userview , CreateUserView

urlpatterns = [
    path('home', Userview.as_view()),
    path('create-user', CreateUserView.as_view()),
    path('List',Userview.as_view()),
    path('detail', SpecificView.as_view())
]
