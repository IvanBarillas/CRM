# users/serializers.py
from rest_framework import serializers
from .models import EndUser, ManagerUser, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['organization', 'phone_number', 'address', 'state', 'zip_code', 'country', 'avatar']

class EndUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = EndUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = EndUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class ManagerUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = ManagerUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = ManagerUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class RequestAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()
