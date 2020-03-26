from rest_framework import serializers
from users.models import Author
from django.contrib.auth.models import User

# code reference:
# Andreas Poyiatzis; https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ('user_type', 'approved', 'avatar', 'github')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = AuthorSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'url', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Author.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.password = validated_data.get('password', instance.password)
        instance.save()

        profile.user_type = profile_data.get('user_type', profile.user_type)
        profile.approved = profile_data.get('approved', profile.approved)
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.github = profile_data.get('github', profile.github)
        profile.save()

        return instance