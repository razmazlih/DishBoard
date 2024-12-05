from django.contrib import admin
from .models import Restaurant, OpeningHours


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address")
    search_fields = ("name", "city", "address")
    list_filter = ("city",)
    ordering = ("name",)


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "day_of_week", "is_open", "opening_time", "closing_time")
    search_fields = ("restaurant__name", "day_of_week")
    list_filter = ("restaurant", "day_of_week", "is_open")
    ordering = ("restaurant", "day_of_week")