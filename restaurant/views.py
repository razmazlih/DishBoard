from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import OpeningHours, Restaurant
from .serializers import OpeningHoursSerializer, RestaurantSerializer
import cloudinary
from datetime import datetime
from django.utils.timezone import make_aware


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
    
    def when_open(self, request, *args, **kwargs):
        restaurant_id = self.request.query_params.get("restaurant_id")
        if not restaurant_id:
            raise ValidationError({"detail": "The 'restaurant_id' parameter is required."})

        now = make_aware(datetime.now())
        current_day = now.strftime('%A')
        current_time = now.time()

        today_hours = OpeningHours.objects.filter(
            restaurant__id=restaurant_id,
            day_of_week=current_day
        ).first()

        if today_hours and today_hours.is_open:
            opening_time = today_hours.opening_time
            closing_time = today_hours.closing_time

            if opening_time <= current_time <= closing_time:
                return Response({
                    "is_open": True,
                    "closes_at": closing_time
                })

        next_day_hours = self.get_next_opening_time(restaurant_id, current_day)

        if next_day_hours:
            return Response({
                "is_open": False,
                "opens_at": next_day_hours["opening_time"],
                "next_day": next_day_hours["day_of_week"]
            })

        return Response({
            "is_open": False,
            "message": "No opening hours available."
        })

    def get_next_opening_time(self, restaurant_id, current_day):
        days_of_week = [
            "Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"
        ]

        current_index = days_of_week.index(current_day)
        for i in range(1, 8):  # בדיקה בשבוע הקרוב
            next_day_index = (current_index + i) % 7
            next_day = days_of_week[next_day_index]

            next_day_hours = OpeningHours.objects.filter(
                restaurant__id=restaurant_id,
                day_of_week=next_day,
                is_open=True
            ).first()

            if next_day_hours:
                return {
                    "day_of_week": next_day,
                    "opening_time": next_day_hours.opening_time
                }

        return None
        