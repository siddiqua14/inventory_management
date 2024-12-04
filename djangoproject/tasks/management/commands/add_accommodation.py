from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from tasks.models import Location, Accommodation
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add accommodation entries to the database'

    def handle(self, *args, **kwargs):
        # Retrieve country locations by country code
        india = Location.objects.filter(location_type="country", country_code="IN").first()
        if not india:
            self.stdout.write(self.style.ERROR('Country location with country code "IN" does not exist'))
            return

        us = Location.objects.filter(location_type="country", country_code="US").first()
        if not us:
            self.stdout.write(self.style.ERROR('Country location with country code "US" does not exist'))
            return

        france = Location.objects.filter(location_type="country", country_code="FR").first()
        if not france:
            self.stdout.write(self.style.ERROR('Country location with country code "FR" does not exist'))
            return

        # Retrieve a test user or create one if it doesn't exist
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No user found in the database'))
            return

        # Helper function to create accommodations if they don't already exist
        def create_accommodation(accommodation_id, **kwargs):
            if not Accommodation.objects.filter(id=accommodation_id).exists():
                Accommodation.objects.create(id=accommodation_id, **kwargs)
                self.stdout.write(self.style.SUCCESS(f'Created accommodation: {accommodation_id}'))
            else:
                self.stdout.write(self.style.WARNING(f'Accommodation with id {accommodation_id} already exists'))

        # Add accommodations
        create_accommodation(
            "IN_MUM_001",  # ID with country and city code
            feed=1,
            title="Cozy Apartment in Mumbai",
            country_code="IN",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(72.8777, 19.0760),
            location=india,  # Associate with India's location
            images=["https://example.com/hotel1.jpg", "https://example.com/hotel2.jpg"],
            amenities=["WiFi", "Air Conditioning", "Hot Water"],
            user=user,
            published=True
        )

        create_accommodation(
            "US_LA_001",  # ID with country and city code
            feed=1,
            title="Luxury Condo in Los Angeles",
            country_code="US",
            bedroom_count=3,
            review_score=4.8,
            usd_rate=250.00,
            center=Point(-118.2437, 34.0522),
            location=us,  # Associate with United States' location
            images=["https://example.com/hotel1.jpg", "https://example.com/hotel2.jpg"],
            amenities=["Pool", "Gym", "Parking"],
            user=user,
            published=True
        )

        create_accommodation(
            "US_NYC_001",  # ID with country and city code
            feed=1,
            title="Modern Apartment in New York City",
            country_code="US",
            bedroom_count=2,
            review_score=4.7,
            usd_rate=300.00,
            center=Point(-74.0060, 40.7128),
            location=us,  # Associate with United States' location
            images=["https://example.com/hotel1.jpg", "https://example.com/hotel2.jpg"],
            amenities=["WiFi", "Heating", "Washer"],
            user=user,
            published=True
        )

        

        self.stdout.write(self.style.SUCCESS('Accommodation entries checked and added'))
