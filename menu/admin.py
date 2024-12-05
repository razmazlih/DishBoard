from django.contrib import admin
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant")
    search_fields = ("name", "restaurant__name")
    list_filter = ("restaurant",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "description")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_available")
    ordering = ("category", "name")