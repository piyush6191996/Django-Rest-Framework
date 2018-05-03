from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# # Create your models here.


class Child(models.Model):
    GENDER_CHOICES =(
        ('M', 'Male'),
        ('F', 'Female')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child')
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Tweets(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    tweets = models.TextField()
    sentiment = models.CharField(max_length=255)




#
# class ProfileModelManager(models.Manager):
#     def _create_auth_token(self, user):
#         Token.objects.get_or_create(user=user)
#         return user.auth_token.key
#
#     def _delete_auth_token(self,user):
#         return Token.objects.get(user=user).delete()
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     auth_token = models.CharField(max_length=255)
#     objects = ProfileModelManager
#
#     def __str__(self):
#         return self.user.username


# Create your models here.
# class ProfileModelManager(models.Manager):
#     def _create_auth_token(self, user):
#         Token.objects.get_or_create(user=user)
#         return user.auth_token.key
#
#     def _delete_auth_token(self, user):
#         return Token.objects.get(user=user).delete()


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     auth_token = models.CharField(max_length=255)
#     # objects = ProfileModelManager()
#
#     def __str__(self):
#         return self.user.username