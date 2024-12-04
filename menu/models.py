from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "restaurant"],
                name="unique_category_name_per_restaurant",
            )
        ]


class Item(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(default="אין תיאור זמין")
    is_available = models.BooleanField(default=True)
    catagory = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="items"
    )

    def __str__(self):
        return f"{self.name} ({self.category.name}) - {self.is_available}"