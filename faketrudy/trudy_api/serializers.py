# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Child, Tweets
from rest_framework.serializers import (
                ModelSerializer,
                CharField,
                Serializer,
                ValidationError,
)


User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            # 'email',
            'password',
        ]
        extra_kwargs = dict(password={'write_only': True})

    def create(self, validated_data):
        print(validated_data)
        print(self)
        username = validated_data['username']
        # email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username
            # email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        # profile = Profile.objects.create(user=user_obj, auth_token=Token.objects.get_or_create(user=user_obj)[0].key)
        # profile.save()
        return user_obj

        # user = User.objects.create_user(username=validated_data['username'],
        #                                 password=validated_data['password'],
        #                                 email=validated_data['email'])
        # user.save()
        # profile = Profile.objects.create(user=user)
        # profile.save()
        # return profile


class UserLoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = 'User is denied permission.'
                    raise ValidationError(msg, code='authorization')

            else:
                msg = 'Unable to login with provided credentials.'
                raise ValidationError(msg, code='authorization')

        else:
            msg = 'Username and Password are required.'
            raise ValidationError(msg, code='authorization')

        user = User.objects.get(id=user.id)
        # profile = Profile.objects.get(user=user)
        Token.auth_token = Token.objects.get_or_create(user=user)[0].key
        attrs['user'] = user
        attrs['token'] = Token.objects.get(user=user).auth_token
        print(attrs)
        return attrs


class UserLogoutSerializer(Serializer):
    def validate(self, attrs):
        user = self.context['request'].user
        if user.auth_token.key:
            user.auth_token.delete()
        else:
            msg = 'User is not logged in.'
            return ValidationError(msg, code='authorization')
        return attrs


class ChildSerializer(ModelSerializer):

    class Meta:
        model = Child
        fields = [
            'name',
            'age',
            'gender',
            'oauth_token',
            'oauth_secret',
        ]

    def create(self, validated_data):
            name = validated_data['name']
            age = validated_data['age']
            gender = validated_data['gender']
            user = validated_data['user']

            child_obj = Child(
                name=name,
                age=age,
                gender=gender,
                user=user
            )

            try:
                oauth_token = validated_data['oauth_token']
                oauth_secret = validated_data['oauth_secret']
                child_obj.twitter_token = oauth_token
                child_obj.twitter_token = oauth_secret
            except:
                pass

            child_obj.save()
            return child_obj


class TweetsSerializer(ModelSerializer):
    pass
    # class Meta:
    #     model = Tweets
    #     fileds = [
    #         'tweets',
    #         'sentiments'
    #     ]
    #
    # def create(self, validated_data):
    #     tweets = validated_data['tweets']
    #     sentiments = validated_data['sentiments']
    #
    #     tweets_obj = Tweets(
    #         tweets=tweets,
    #         sentiments=sentiments
    #     )
    #     tweets_obj.save()
    #     return tweets_obj
