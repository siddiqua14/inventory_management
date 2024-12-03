from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from tasks.models import Accommodation, Location, LocalizeAccommodation
from django.contrib.gis.geos import Point

class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="loc1",
            title="Test City",
            location_type="city",
            country_code="US",
            state_abbr="CA",
            city="Test City",
            center="POINT(-118.2437 34.0522)",
        )

    def test_location_creation(self):
        self.assertEqual(self.location.title, "Test City")
        self.assertEqual(self.location.location_type, "city")
        self.assertEqual(self.location.country_code, "US")


class AccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = Location.objects.create(
            id="loc1",
            title="Test City",
            location_type="city",
            country_code="US",
            state_abbr="CA",
            city="Test City",
            center="POINT(-118.2437 34.0522)",
        )
        self.accommodation = Accommodation.objects.create(
            id="acc1",
            title="Test Accommodation",
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center="POINT(-118.2437 34.0522)",
            location=self.location,
            user=self.user,
        )

    def test_accommodation_creation(self):
        self.assertEqual(self.accommodation.title, "Test Accommodation")
        self.assertEqual(self.accommodation.review_score, 4.5)
        self.assertEqual(self.accommodation.user.username, "testuser")


class SignupRequestViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        self.assertTrue(User.objects.filter(username="newuser").exists())


class AccommodationAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="apiuser", password="password")
        self.group = Group.objects.create(name="Property Owners")
        self.user.groups.add(self.group)

    def test_authenticated_user_can_access_accommodations(self):
        self.client.login(username="apiuser", password="password")
        response = self.client.get(
            reverse("accommodation-list")
        )  # Using router basename
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_access_accommodations(self):
        response = self.client.get(reverse("accommodation-list"))
        self.assertEqual(response.status_code, 403)  # Update to match the actual response



class LocalizationTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )

        # Create a location
        self.location = Location.objects.create(
            id="loc1",
            title="Sample City",
            center=Point(90.4125, 23.8103),  # Example coordinates for Dhaka
            location_type="city",
            country_code="BD",
            city="Dhaka",
        )

        # Create an accommodation
        self.accommodation = Accommodation.objects.create(
            id="acc1",
            title="Luxury Suite",
            country_code="BD",
            bedroom_count=2,
            review_score=4.8,
            usd_rate=120.50,
            center=Point(90.4125, 23.8103),
            location=self.location,
            user=self.user,
            published=True,
        )

        # Create localizations for the accommodation
        self.localization_en = LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="en",
            description="A luxurious suite with modern amenities.",
            policy={"pet_policy": "No pets allowed"},
        )
        self.localization_fr = LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="fr",
            description="Une suite luxueuse avec des équipements modernes.",
            policy={"pet_policy": "Animaux interdits"},
        )

    def test_localization_creation(self):
        # Test if localization records are created correctly
        self.assertEqual(LocalizeAccommodation.objects.count(), 2)
        self.assertEqual(self.localization_en.property.title, "Luxury Suite")
        self.assertEqual(self.localization_en.language, "en")
        self.assertEqual(
            self.localization_en.description, "A luxurious suite with modern amenities."
        )

    def test_localized_descriptions(self):
        # Test localized descriptions
        en_localization = LocalizeAccommodation.objects.get(language="en")
        fr_localization = LocalizeAccommodation.objects.get(language="fr")
        self.assertEqual(
            en_localization.description, "A luxurious suite with modern amenities."
        )
        self.assertEqual(
            fr_localization.description,
            "Une suite luxueuse avec des équipements modernes.",
        )

    def test_localization_policy(self):
        # Test if policy JSON is stored and retrieved correctly
        self.assertEqual(self.localization_en.policy["pet_policy"], "No pets allowed")
        self.assertEqual(self.localization_fr.policy["pet_policy"], "Animaux interdits")
