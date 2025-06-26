from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    """
    Custom user model for Users, extending Django's AbstractUser.
    This allows for additional fields specific to hikers in the future.
    """
    username = models.CharField(max_length=255, unique=True,)
    email = models.EmailField(unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    """
    Profile model for additional user information.
    This can include fields like bio, profile picture, etc.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_photo = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance whenever a User is created.
    """
    if created:
        Profile.objects.create(user=instance)
        
post_save.connect(create_user_profile, sender=User)