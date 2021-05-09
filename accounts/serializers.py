# accounts.serializers.py
# 
from rest_framework import serializers
from django.contrib.auth.models import User

# the fields included here are the data from the models you want to send back as Json data, through the views.py
# they don't have to include EVERY field. can exclude as you wish. 
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', "is_staff")

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
