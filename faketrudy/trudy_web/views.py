from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from pip._vendor import requests
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from trudy_api.models import Child
# from faketrudy.faketrudy import settings
from django.conf import settings
import oauth2 as oauth

# Create your views here.



def login(request):
    """
    Login user by adding token to cookies
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            token = Token.objects.get(user=user)
            key = token.key
            if key:
                response = redirect('trudy_web:home')
                response.set_cookie('currentuser', key)
                return response
    else:
        print('direct')
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # email = request.POST['email']

        payload = {'username': username, 'password': password}
        obj = requests.post('http://127.0.0.1:8000/register', data=payload).json()
        print(obj)
        # return HttpResponse("hello")
        token = Token.objects.create(user=username)
        key = token.key
        if key:
            response = redirect('trudy_web:home')
            response.set_cookie('currentuser', key)
            return response
    else:
        return render(request, 'login.html')


def logout(request):
    """
    Logout a user by removing cookie
    """
    # token = Token.objects.all()
    # print(token)
    # users = User.objects.all()
    asd = request.COOKIES
    print(asd)
    # for user in users:
    #     print('in for loop')
    if 'currentuser' in asd:
            print('in if')
            response = HttpResponse("Successfully logged out")
            response.delete_cookie('currentuser')
            return response
    return HttpResponse("User not Found, maybe he is not already logged in")



def home(request):
    """
    Home
    """
    cookie = request.COOKIES
    if 'currentuser' in cookie:
        if request.method == 'POST':
            token = cookie['currentuser']
            header = 'Token ' + token
            print(token)
            user = User.objects.get(username=Token.objects.get(key=token).user)
            children = user.child.all()
            name = request.POST['name']
            age = int(request.POST['age'])
            gender = request.POST['gender']
            print(gender)

            payload = {'user': user, 'name': name, 'age': age, 'gender': gender}
            obj = requests.post('http://127.0.0.1:8000/child', data=payload, headers={'Authorization': header}).json()
            print(obj)

            return render(request, 'home.html', {'user': user, 'children': children})
        else:
            token = cookie['currentuser']
            user = User.objects.get(username=Token.objects.get(key=token).user)
            children = user.child.all()
            return render(request, 'home.html', {'user':user, 'children': children})
    else:
        return HttpResponse('You are not logged in :-( ')


def child(request, pk):
    child = Child.objects.get(pk=pk)
    return render(request, 'child.html', {'child': child})


def twitter(request):
    consumer = oauth.Consumer(key=settings.CONSUMER_KEY, secret=settings.CONSUMER_SECRET)
    access_token = oauth.Token(key=settings.ACCESS_KEY, secret=settings.ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    print(consumer)
    print(access_token)
    print(client)

    return HttpResponse('test')
