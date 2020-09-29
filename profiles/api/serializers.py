from profiles.models import SellerProfile, ClientProfile
from rest_framework import serializers, status
# from models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.response import Response
from django.http import JsonResponse
# from rest_framework import status

from rest_framework import status
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    def save(self, *args, **kwargs):
        print("save method called")
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            # first_name=self.validated_data['first_name'],
            # last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'password must match'})
        user.set_password(password)
        user.save()
        return user

    # def __str__(self):
    #     return self.user


# class UserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='password',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password')

#     def create(self, validated_data):
#         user = UserModel.objects.create(
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


# class ClientSerializer(serializers.ModelSerializer):

#     user = UserSerializer(required=True)

#     class Meta:
#         model = ClientProfile
#         fields = ['user']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(
#             UserSerializer(), validated_data=user_data)
#         buyer, created = ClientProfile.objects.update_or_create(
#             user=user,
#             # mobileNo=validated_data.pop('mobileNo'),
#             # location=validated_data.pop('location'),
#             # address=validated_data.pop('address'),

#         )
#         return buyer


class SellerSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = SellerProfile
        fields = ('user', 'mobileNo', 'cnic',
                  'city', 'address', 'state', 'shop_name')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        seller, created = SellerProfile.objects.update_or_create(user=user,
                                                                 mobileNo=validated_data.pop(
                                                                     'mobileNo'),
                                                                 cnic=validated_data.pop(
                                                                     'cnic'),
                                                                 city=validated_data.pop(
                                                                     'city'),
                                                                 address=validated_data.pop(
                                                                     'address'),
                                                                 shop_name=validated_data.pop(
                                                                     'shop_name'),
                                                                 state=validated_data.pop(
                                                                     'state'
                                                                 )
                                                                 )

        return seller
