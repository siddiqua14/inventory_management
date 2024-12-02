from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LocationAPI, AccommodationAPI, SignupRequestView
from django.contrib.auth.views import LoginView  # Import the LoginView

router = DefaultRouter()
router.register("locations", LocationAPI, basename="locations")
router.register("accommodations", AccommodationAPI, basename="accommodation")

urlpatterns = [
    path('', SignupRequestView.as_view(), name='signup'),  # Landing page for /tasks
    path('login/', LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('', include(router.urls)),  # Include router URLs
]
