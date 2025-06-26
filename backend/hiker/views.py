from django.shortcuts import render
from .models import User, Profile
from .serializers import UserSerializer, TokenObtainPairSerializerWithUser, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

class TokenObtainPairSerializerWithUser(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens with user information.
    """
    serializer_class = TokenObtainPairSerializerWithUser
    
class RegisterView(generics.CreateAPIView):
    """
    View to handle user registration.
    Uses RegisterSerializer to validate and create a new user.
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = ([AllowAny])  # No permissions required for registration
    
    
class UserListView(generics.ListAPIView):
    """
    View to list all users.
    Requires authentication.
    """
    serializer_class = UserSerializer
    permission_classes = ([AllowAny])
    queryset = User.objects.all()
    

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a user.
    Requires authentication.
    """
    serializer_class = UserSerializer
    permission_classes = ([IsAuthenticated])
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user
    

    