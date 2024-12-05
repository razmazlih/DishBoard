from rest_framework import serializers
from .models import Restaurant, OpeningHours


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ["id", "restaurant", "day_of_week", "is_open", "opening_time", "closing_time"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "city", "address"]