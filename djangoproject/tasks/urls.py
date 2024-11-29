from rest_framework.routers import DefaultRouter
from .views import LocationAPI, AccommodationAPI

router = DefaultRouter()
router.register("locations", LocationAPI, basename="locations")
router.register("accommodations", AccommodationAPI, basename="accommodation")
urlpatterns = router.urls
