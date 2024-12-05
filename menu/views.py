from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from menu.models import Category, Item
from rest_framework.response import Response
from menu.serializers import CategorySerializer, ItemSerializer
from rest_framework import status


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        restaurant_id = request.query_params.get("restaurant_id")
        if not restaurant_id:
            return Response(
                {"detail": "יש לספק restaurant_id כפרמטר בשורת הכתובת."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        categories = self.queryset.filter(restaurant_id=restaurant_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "קריאת רשימת פריטים אינה נתמכת."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
