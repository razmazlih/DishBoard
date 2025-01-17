from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    photo = CloudinaryField('image', blank=True, null=True)
    photo_url = models.CharField(
        max_length=200,
        default="https://res.cloudinary.com/drlmg8tzf/image/upload/v1736885696/py7lepbjsndwwwt7nszs.jpg",
    )

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
    opening_time = models.TimeField(default="00:00")
    closing_time = models.TimeField(default="00:00")

    class Meta:
        unique_together = ("restaurant", "day_of_week")

    def __str__(self):
        if self.is_open:
            return f"{self.restaurant.name} - {self.day_of_week}: {self.opening_time} - {self.closing_time}"
        return f"{self.restaurant.name} - {self.day_of_week}: Closed"


@receiver(post_save, sender=Restaurant)
def create_opening_hours(sender, instance, created, **kwargs):
    if created:
        days = OpeningHours.DAYS_OF_WEEK

        for day in days:
            OpeningHours.objects.create(
                restaurant=instance,
                day_of_week=day[0],
            )
