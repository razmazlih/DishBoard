from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from menu.models import Category
from rest_framework.response import Response
from menu.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"], url_path="by-restaurant/(?P<restaurant_id>[^/.]+)")
    def by_restaurant(self, request, restaurant_id=None):
        categories = self.queryset.filter(restaurant_id=restaurant_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)