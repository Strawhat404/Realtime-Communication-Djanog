from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'beacons', views.BeaconDeviceViewSet)
router.register(r'events', views.ProximityEventViewSet, basename='events')
router.register(r'notifications',views.NotificationViewSet, basename='notifications')

urlpatterns = [
    path('',include(router.urls)),
]