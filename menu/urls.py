from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'item', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]