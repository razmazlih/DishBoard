from rest_framework.viewsets import ModelViewSet
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer