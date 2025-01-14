from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import OpeningHours, Restaurant
from .serializers import OpeningHoursSerializer, RestaurantSerializer
import cloudinary


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        image_file = self.request.FILES.get('photo')
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            photo_url = upload_result.get('secure_url')
        else:
            photo_url = "https://res.cloudinary.com/drlmg8tzf/image/upload/v1736885696/py7lepbjsndwwwt7nszs.jpg"
    
        serializer.save(photo_url=photo_url)

    def perform_update(self, serializer):
        image_file = self.request.FILES.get('photo')
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            photo_url = upload_result.get('secure_url')
            serializer.save(photo_url=photo_url)
        else:
            serializer.save()

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
