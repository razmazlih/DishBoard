from rest_framework import serializers
from .models import Category, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "category", "name", "price", "description", "is_available"]


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id", "restaurant", "name", 'items']

    def update(self, instance, validated_data):
        validated_data.pop('restaurant', None)
        return super().update(instance, validated_data)