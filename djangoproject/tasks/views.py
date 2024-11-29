from rest_framework.viewsets import ModelViewSet
from .models import Location, Accommodation  # Use Location instead of Task
from .serializers import LocationSerializer, AccommodationSerializer  # Import the new Location serializer

class LocationAPI(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class AccommodationAPI(ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer