from django.urls import include, path
from rest_framework import routers
from .views import SensorViewSet, LecturaViewSet

router = routers.DefaultRouter()
router.register(r'sensores', SensorViewSet)
router.register(r'lecturas', LecturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
