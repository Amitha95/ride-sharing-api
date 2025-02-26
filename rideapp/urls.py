from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, RideViewSet

# Register RideViewSet using DefaultRouter
router = DefaultRouter()
router.register(r'rides', RideViewSet)  # Now available at `/api/rides/`

user_list = UserViewSet.as_view({'post': 'register'})
user_login = UserViewSet.as_view({'post': 'login'})

urlpatterns = [
    path('users/register/', user_list, name='register'),
    path('users/login/', user_login, name='login'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Include the router URLs
]
