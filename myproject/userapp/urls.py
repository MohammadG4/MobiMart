from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
path('profile/', views.GetProfile.as_view(), name='user-profile'),
path('logout/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='logout'),
]

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
urlpatterns += router.urls