from django.shortcuts import render

# Create your views here.
# accounts.views.py

# Here, we are adding all of the necessary imports for our LoginView
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer
from django.contrib.auth.models import User # the default User model from django
from django.contrib.auth import authenticate, login, logout

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

    def post(self, request, *args, **kwargs): # deals with a POST request
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None: # a user object is returned as it exists
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            refresh = RefreshToken.for_user(user)
            token_serializer = TokenSerializer(data={
                # using DRF JWT utility functions to generate a token
                "token": str(refresh.access_token),
                })
            token_serializer.is_valid()
            user_serializer = UserSerializer(user)
            return Response(
                data={
                    **token_serializer.data, # python "unpacking", similar to spread operator "..." in JS.
                    "data": user_serializer.data,
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
            print(f"adasdasdasdasdasdasdasd {new_user}")
            return Response(data={
                "success": True,
                "message": f"{new_user} successfully created"
            },
                status=status.HTTP_201_CREATED)
            
        
class EditUsersView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "username" # query by the username to find details and update or delete. recall that lookup_field must correspond with the param in the url for this view
    
    def put(self, request, *args, **kwargs):
    
        user_id = request.data.get("id", "")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        
        # print(request.data)
        
        if not username or not password or not email: # ensures all fields are filled
                return Response(
                    data={
                        "message": "username, password and email is required to edit user details",
                        "success": False
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            existing_user = User.objects.get(pk=user_id)
            existing_user.username = username # you can only access django objects using dot notation. wtF
            existing_user.email = email
            existing_user.set_password(password) #using the django helper function to reset the password using new input
            existing_user.save()
            
            user_serializer = UserSerializer(existing_user)
            return Response(
                data={
                    "data": user_serializer.data,
                    "message": f"'{existing_user}' updated successfully",
                    "success": True
                },
                status=status.HTTP_200_OK
            )
        

class LogoutView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def post(self, request, *args, **kwargs):
        # use django's session framework to log out
        # remember to DESTROY the JWT on the client localstorage upon logout
        logout(request)
        
        return Response(data={
            "success": True,
            "message": "Logged Out Successfully"
        })