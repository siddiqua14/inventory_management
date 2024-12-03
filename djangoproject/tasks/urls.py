from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LocationAPI, AccommodationAPI, SignupRequestView

router = DefaultRouter()
router.register("locations", LocationAPI, basename="locations")
router.register("accommodations", AccommodationAPI, basename="accommodation")

urlpatterns = [
    path('', SignupRequestView.as_view(), name='signup'),  # Landing page for /tasks
    #path('', include(router.urls)),  # Include router URLs
    path('tasks/', include(router.urls)),
]
