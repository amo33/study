from curses.ascii import SP
from django.urls import path
from .views import UserView

urlpatterns = [
    path('user', UserView.as_view()),
    path('user/<path:datatype>', UserView.as_view()),
]
