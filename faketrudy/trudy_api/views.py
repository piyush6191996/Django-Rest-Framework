from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .models import Child, Tweets
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserLogoutSerializer, ChildSerializer, TweetsSerializer
# Create your views here.

User = get_user_model()


class UserRegistrationAPIView(APIView):
    """
    Register a User
    """
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] = token.key
            return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
    Retrieve auth token for a user
    """
    serializer_class = UserLoginSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
                return Response({'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """
    Delete the auth token for a logged in User.
    """

    authentication_classes = (TokenAuthentication,)
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ChildAPIView(APIView):

    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):

        token = self.request.META.get('HTTP_AUTHORIZATION')
        token = token.split()
        token = token[1]
        token = Token.objects.get(key=token)
        user = token.user

        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


