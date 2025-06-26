from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    This serializer includes fields for username and email.
    """
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)
    bio = serializers.CharField(source="profile.bio", read_only=True)
    profile_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_photo')
        
    def get_profile_photo(self, obj):
        if obj.profile.profile_photo:
            return obj.profile.profile_photo.url
        return None
        
class TokenObtainPairSerializerWithUser(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer to include user information in the token response.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.profile.first_name 
        token['last_name'] = user.profile.last_name
        token['bio'] = user.profile.bio
        token['profile_photo'] = user.profile.profile_photo.url if user.profile.profile_photo else None
        token['is_active'] = user.profile.is_active
        
        # Log the token creation for debugging purposes
        print("Token obtained with user information:", token)
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password and creates a new user instance.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
              
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        
    def validate(self, attrs):
        """
        Validate that the two password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password": "Password fields do not match."})
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user instance.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user