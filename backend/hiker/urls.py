from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TokenObtainPairSerializerWithUser, RegisterView, UserListView
from hiker import views


urlpatterns = [
    path('token/', TokenObtainPairSerializerWithUser.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

]