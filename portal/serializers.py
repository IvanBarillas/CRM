# portal/serializers.py
from rest_framework import serializers

class RequestAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()
