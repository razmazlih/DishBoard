from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import OpeningHours, Restaurant
from .serializers import OpeningHoursSerializer, RestaurantSerializer


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def list(self, request, *args, **kwargs):
        fields = request.query_params.get("fields", None)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if fields:
            if "id" not in fields:
                fields = "id," + fields

            fields = fields.split(",")
            data = [
                {field: item[field] for field in fields if field in item}
                for item in serializer.data
            ]
            return Response(data)

        return Response(serializer.data)


class OpeningHouersViewSet(ModelViewSet):
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get("restaurant_id")
        if not restaurant_id:
            raise ValidationError({"detail": "The 'restaurant_id' parameter is required."})

        queryset = super().get_queryset()

        queryset = queryset.filter(restaurant__id=restaurant_id)
        return queryset
