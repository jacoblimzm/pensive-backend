from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from .models import BlogEntry, Category
from .serializers import BlogEntrySerializer, CategorySerialiser

from django.contrib.auth.models import User # the default User model from django
from django.contrib.auth import authenticate, login



class BlogEntryListView(generics.ListAPIView):
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug" # this tells the view class to lookup the list of posts using the "slug" property instead of the usual pk
    permission_classes = (permissions.AllowAny,)

    
