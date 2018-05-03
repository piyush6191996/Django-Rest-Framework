from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'trudy_api'

urlpatterns = [
    path('register', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login', views.UserLoginAPIView.as_view(), name='login'),
    path('logout', views.UserLogoutAPIView.as_view(), name='logout'),
    path('child', views.ChildAPIView.as_view(), name='child'),
]

