from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LocationAPI, AccommodationAPI, SignupRequestView

router = DefaultRouter()
router.register("locations", LocationAPI, basename="locations")
router.register("accommodations", AccommodationAPI, basename="accommodation")

urlpatterns = router.urls  # Keep the router URLs
urlpatterns = [
    path('signup/', SignupRequestView.as_view(), name='signup'),  # Add the signup URL here
]
