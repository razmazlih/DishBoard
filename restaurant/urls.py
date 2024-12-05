from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OpeningHouersViewSet, RestaurantViewSet

router = DefaultRouter()
router.register(r'info', RestaurantViewSet, basename='restaurant')
router.register(r'opening-houers', OpeningHouersViewSet, basename='opening_houers')

urlpatterns = [
    path('', include(router.urls)),
]