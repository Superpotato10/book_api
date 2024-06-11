from django.urls import path, include
from rest_framework import routers

from orders.viewsets import OrderViewSet

app_name = 'orders'

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
