from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView  # Import TemplateView
from .models import Accommodation, Location
from .serializers import AccommodationSerializer, LocationSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import NotAuthenticated
from django.contrib import messages

class LocationAPI(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class AccommodationAPI(ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Property Owners").exists():
            return Accommodation.objects.filter(user=self.request.user)
        return super().get_queryset()

    def permission_denied(self, request, message=None, code=None):
        if not request.user.is_authenticated:
            raise NotAuthenticated(
                detail="Authentication credentials were not provided."
            )
        super().permission_denied(request, message=message, code=code)




class SignupRequestView(TemplateView):
    template_name = "tasks/signup.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        group_name = "Property Owners"

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, self.template_name)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, self.template_name)

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.is_active = False
        user.save()

        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        messages.success(request, "Signup successful! Please wait for admin approval.")
        return redirect("/admin/login/")  # Redirect to login page

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  # Ensure no lingering messages
