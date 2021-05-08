from django.shortcuts import render

# Create your views here.
# accounts.views.py

# Here, we are adding all of the necessary imports for our LoginView
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer
from django.contrib.auth.models import User # the default User model from django
from django.contrib.auth import authenticate, login

# JWT settings
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(generics.ListCreateAPIView):
    """
    POST user/login/
    """

    # This permission class will overide the global permission class setting
    # Permission checks are always run at the very start of the view, before any other code is allowed to proceed.
    # The permission class here is set to AllowAny, which overwrites the global class to allow anyone to have access to login.
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None: # a user object is returned as it exists
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serializer = TokenSerializer(data={
                # using DRF JWT utility functions to generate a token
                "token": str(refresh.access_token),
                })
            serializer.is_valid()
            return Response(
                data={
                    **serializer.data, # python "unpacking", similar to spread operator "..." in JS.
                    "message": "successfully logged in!",
                    "success": True,
                    }
                )
        return Response(
            data={
                "message": f"login is unsuccessful, please try again",
                "success": False,
                },
            status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterUsersView(generics.ListCreateAPIView):
    """
    POST user/signup/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def post(self, request, *args, **kwargs):
    #     username = request.data.get("username", "")
    #     password = request.data.get("password", "")
    #     email = request.data.get("email", "")
        
    #     result = User.objects.get(username=username) # checks to see if user already exists
    #     print(f"adasdasdasdasdasdasdasd {result}") 
        
    #     if not username or not password or not email:
    #         return Response(
    #             data={
    #                 "message": "username, password and email is required to register a user",
    #                 "success": False
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     elif result:
    #         return Response(data={
    #             "success": False,
    #             "message": f"{username} is not available"
    #         })
    #     else:
    #         new_user = User.objects.create_user(
    #                 username=username, password=password, email=email
    #         )
    #         print(f"adasdasdasdasdasdasdasd {new_user}");
    #         return Response(status=status.HTTP_201_CREATED)
        
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        
        if not username or not password or not email: # ensures all fields are filled
                return Response(
                    data={
                        "message": "username, password and email is required to register a user",
                        "success": False
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        try: 
            result = User.objects.get(username=username) # checks to see if user already exists, throws a DoesNotExist Error if a user is not found
            print(f"adasdasdasdasdasdasdasd {result}") 
            if result:
                return Response(data={
                    "success": False,
                    "message": f"{username} is not available"
                })
                
        except User.DoesNotExist:
            new_user = User.objects.create_user(
                    username=username, password=password, email=email
            )
            print(f"adasdasdasdasdasdasdasd {new_user}");
            return Response(data={
                "success": True,
                "message": f"{new_user} successfully created"
            },
                status=status.HTTP_201_CREATED)
            
        
