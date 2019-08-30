__author__ = 'dmalik'
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import CustomLoginView

urlpatterns = [

    path('login/', CustomLoginView.as_view(
        template_name='authentication/login.html'
    ), name="login"),

    path('logout/', LogoutView.as_view(
    ), name="logout"),

]


