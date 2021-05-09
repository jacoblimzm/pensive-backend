from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from .models import BlogEntry, Category
from .serializers import BlogEntrySerializer, CategorySerializer

from django.contrib.auth.models import User # the default User model from django
from django.contrib.auth import authenticate, login


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)   
    
class CategoryDetailView(generics.RetrieveAPIView): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "category_name" # returns the individual category along with all related posts
    permission_classes = (permissions.AllowAny,)

class BlogEntryListView(generics.ListAPIView):
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug" # this tells the view class to lookup the list of posts using the "slug" property instead of the usual pk
    permission_classes = (permissions.AllowAny,)

class BlogEntryDetailView(generics.RetrieveAPIView): # "retrieveAPIview" always needs a lookup field which must correspond to the url param in urls.py. retrive is a specific search for 1 it
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug"
    permission_classes = (permissions.AllowAny,)
    
class BlogEntryBreakingView(generics.ListAPIView):
    queryset = BlogEntry.objects.all().filter(breaking=True)
    serializer_class = BlogEntrySerializer
    lookup_field = "slug"
    permission_classes = (permissions.AllowAny,)
    
class BlogEntryCreateView(generics.ListCreateAPIView):
    
    """
    POST new/
    """
    
    queryset = BlogEntry.objects.all()
    serializer_class = BlogEntrySerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        
        print(request.data)
        pass
        
        return Response (data={
            "success": True,
            "message": "post has been created successfully!"
        })
        # if not username or not password or not email: # ensures all fields are filled
        #         return Response(
        #             data={
        #                 "message": "username, password and email is required to register a user",
        #                 "success": False
        #             },
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        # try: 
        #     result = User.objects.get(username=username) # checks to see if user already exists, throws a DoesNotExist Error if a user is not found
        #     print(f"adasdasdasdasdasdasdasd {result}") 
        #     if result:
        #         return Response(data={
        #             "success": False,
        #             "message": f"{username} is not available"
        #         })
                
        # except User.DoesNotExist:
        #     new_user = User.objects.create_user(
        #             username=username, password=password, email=email
        #     )
        #     print(f"adasdasdasdasdasdasdasd {new_user}")
        #     return Response(data={
        #         "success": True,
        #         "message": f"{new_user} successfully created"
        #     },
        #         status=status.HTTP_201_CREATED)
    
    
    
    