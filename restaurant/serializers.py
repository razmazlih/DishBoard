from rest_framework import serializers
from .models import Restaurant, OpeningHours


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ["day_of_week", "is_open", "opening_time", "closing_time"]

    def validate(self, data):
        if data.get("is_open") and (not data.get("opening_time") or not data.get("closing_time")):
            raise serializers.ValidationError(
                "Opening and closing times must be provided if the restaurant is open."
            )
        return data


class RestaurantSerializer(serializers.ModelSerializer):
    opening_hours = OpeningHoursSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "city", "address", "opening_hours"]

    def update(self, instance, validated_data):
        opening_hours_data = validated_data.pop("opening_hours", [])
        instance.name = validated_data.get("name", instance.name)
        instance.city = validated_data.get("city", instance.city)
        instance.address = validated_data.get("address", instance.address)
        instance.save()

        # עדכון שעות פתיחה
        existing_hours = {oh.day_of_week: oh for oh in instance.opening_hours.all()}
        for oh_data in opening_hours_data:
            day_of_week = oh_data.get("day_of_week")
            if not day_of_week:
                raise serializers.ValidationError("Each opening hour entry must include 'day_of_week'.")
            
            if day_of_week in existing_hours:
                opening_hour = existing_hours[day_of_week]
                opening_hour.is_open = oh_data.get("is_open", opening_hour.is_open)
                opening_hour.opening_time = oh_data.get("opening_time", opening_hour.opening_time)
                opening_hour.closing_time = oh_data.get("closing_time", opening_hour.closing_time)
                opening_hour.save()

        return instance