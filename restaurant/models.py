from django.db import models
from django.forms import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=30)

    class Meta:
        unique_together = ("name", "address")

    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    DAYS_OF_WEEK = [
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="opening_hours"
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    is_open = models.BooleanField(default=False)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    class Meta:
        unique_together = ("restaurant", "day_of_week")

    def __str__(self):
        if self.is_open:
            return f"{self.restaurant.name} - {self.day_of_week}: {self.opening_time} - {self.closing_time}"
        return f"{self.restaurant.name} - {self.day_of_week}: Closed"

@receiver(post_save, sender=Restaurant)
def create_opening_hours(sender, instance, created, **kwargs):
    if created:
        default_time = "00:00"
        days = OpeningHours.DAYS_OF_WEEK

        for day in days:
            OpeningHours.objects.create(
                restaurant=instance,
                day_of_week=day[0],
                is_open=False,
                opening_time=default_time,
                closing_time=default_time,
            )