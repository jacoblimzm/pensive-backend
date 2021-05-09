# accounts.urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path("user/login/", views.LoginView.as_view(), name="user-login"),
    path("user/logout/", views.LogoutView.as_view(), name="user-logout"),
    path("user/register/", views.RegisterUsersView.as_view(), name="user-register"),
    path("user/edit/<username>", views.EditUsersView.as_view(), name="user-edit"),
]
