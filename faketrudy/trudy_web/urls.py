from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'trudy_web'


urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('child/<int:pk>', views.child, name='child'),
    path('test', views.twitter, name='test'),
]
