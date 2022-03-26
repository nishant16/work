from django.urls import path, include
from rest_framework import routers

from seat_allocation.api.viewsets import (
    AllocationViewset, RoomViewset
)
router = routers.SimpleRouter()
router.register(r'allocation', AllocationViewset, basename='allocation')
router.register(r'room', RoomViewset, basename='room')

urlpatterns = [
    path(r'', include(router.urls)),
]
