from django.urls import path, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from backend_api.views import VehicleViewSet, BookingViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet,  basename='vehicle')
router.register(r'bookings', BookingViewSet,  basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
