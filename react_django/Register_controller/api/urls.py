from django.urls import path
from .views import Userview , CreateUserView

urlpatterns = [
    path('home', Userview.as_view()),
    path('create-user', CreateUserView.as_view())
]