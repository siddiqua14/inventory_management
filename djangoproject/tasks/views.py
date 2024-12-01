from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import Accommodation, Location
from .serializers import AccommodationSerializer, LocationSerializer
from rest_framework import status
from rest_framework.permissions import BasePermission

class LocationAPI(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class IsPropertyOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Property Owners").exists()

class AccommodationAPI(ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated, IsPropertyOwner]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Property Owners").exists():
            return Accommodation.objects.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically assign the logged-in user

class SignupRequestView(APIView):
    def get(self, request, *args, **kwargs):
        # Render the signup form
        return render(request, "signup.html")

    def post(self, request, *args, **kwargs):
        # Use request.data to handle POST data from form or JSON request
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        group_name = "Property Owners"

        if not username or not email or not password:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Get or create the "Property Owners" group
        group, created = Group.objects.get_or_create(name=group_name)
        
        # Add user to the group
        user.groups.add(group)

        return Response({"message": "Signup successful. Please wait for approval."}, status=status.HTTP_201_CREATED)