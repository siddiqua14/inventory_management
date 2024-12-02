from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView  # Import TemplateView
from .models import Accommodation, Location
from .serializers import AccommodationSerializer, LocationSerializer
from rest_framework import status
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponse

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


# Modify SignupRequestView to inherit TemplateView for rendering the template
class SignupRequestView(TemplateView):
    template_name = "tasks/signup.html"  # Template for the signup page

    def post(self, request, *args, **kwargs):
        # Handle the signup form submission
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        group_name = "Property Owners"

        if not username or not email or not password:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Set inactive initially for admin approval
        user.save()

        # Create or get the "Property Owners" group
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # Redirect to a different page (e.g., login page) after successful signup
        return redirect('/admin/login/')  # Assuming 'login' is a named URL pattern for the login page

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to some page after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'tasks/login.html', {'form': form})