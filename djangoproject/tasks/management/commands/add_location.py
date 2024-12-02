from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.gis.geos import Point
from tasks.models import Location

class Command(BaseCommand):
    help = 'Add locations to the database'

    def handle(self, *args, **kwargs):
        # Get the Location model dynamically from the app registry
        Location = apps.get_model('tasks', 'Location')

        # Add Country: India if it doesn't exist
        india, created = Location.objects.get_or_create(
            id="IN",
            defaults={
                'title': "India",
                'center': Point(78.9629, 20.5937),  # Longitude, Latitude for India
                'location_type': "country",
                'country_code': "IN"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('India location created'))
        else:
            self.stdout.write(self.style.SUCCESS('India location already exists'))

        # Add State: Maharashtra (India) if it doesn't exist
        maharashtra, created = Location.objects.get_or_create(
            id="MH",
            defaults={
                'title': "Maharashtra",
                'center': Point(19.2183, 72.9787),  # Longitude, Latitude for Maharashtra
                'location_type': "state",
                'parent': india,  # Set the parent to India
                'state_abbr': "MH",
                'country_code': "IN"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Maharashtra location created'))
        else:
            self.stdout.write(self.style.SUCCESS('Maharashtra location already exists'))

        # Add City: Mumbai (Maharashtra) if it doesn't exist
        mumbai, created = Location.objects.get_or_create(
            id="MUM",
            defaults={
                'title': "Mumbai",
                'center': Point(72.8777, 19.0760),  # Longitude, Latitude for Mumbai
                'location_type': "city",
                'parent': maharashtra,  # Set the parent to Maharashtra
                'city': "Mumbai",
                'state_abbr': "MH",
                'country_code': "IN"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Mumbai location created'))
        else:
            self.stdout.write(self.style.SUCCESS('Mumbai location already exists'))

        # Add Country: United States (US) if it doesn't exist
        us, created = Location.objects.get_or_create(
            id="US",
            defaults={
                'title': "United States",
                'center': Point(-99.9018, 37.0902),  # Longitude, Latitude for US
                'location_type': "country",
                'country_code': "US"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('United States location created'))
        else:
            self.stdout.write(self.style.SUCCESS('United States location already exists'))

        # Add State: California (United States) if it doesn't exist
        california, created = Location.objects.get_or_create(
            id="CA",
            defaults={
                'title': "California",
                'center': Point(-119.4179, 36.7783),  # Longitude, Latitude for California
                'location_type': "state",
                'parent': us,  # Set the parent to United States
                'state_abbr': "CA",
                'country_code': "US"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('California location created'))
        else:
            self.stdout.write(self.style.SUCCESS('California location already exists'))

        # Add City: Los Angeles (California) if it doesn't exist
        los_angeles, created = Location.objects.get_or_create(
            id="LA",
            defaults={
                'title': "Los Angeles",
                'center': Point(-118.2437, 34.0522),  # Longitude, Latitude for Los Angeles
                'location_type': "city",
                'country_code': "US",
                'state_abbr': "CA",
                'city': "Los Angeles",
                'parent': california  # Set the parent to California
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Los Angeles location created'))
        else:
            self.stdout.write(self.style.SUCCESS('Los Angeles location already exists'))

        # Add City: New York City (United States) if it doesn't exist
        new_york_city, created = Location.objects.get_or_create(
            id="NYC",
            defaults={
                'title': "New York City",
                'center': Point(-74.0060, 40.7128),  # Longitude, Latitude for New York City
                'location_type': "city",
                'parent': us,  # Set the parent to United States
                'state_abbr': "NY",
                'country_code': "US",
                'city': "New York City"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('New York City location created'))
        else:
            self.stdout.write(self.style.SUCCESS('New York City location already exists'))

        # Add City: Paris (France) if it doesn't exist
        paris, created = Location.objects.get_or_create(
            id="PAR",
            defaults={
                'title': "Paris",
                'center': Point(2.3522, 48.8566),  # Longitude, Latitude for Paris
                'location_type': "city",
                'country_code': "FR"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Paris location created'))
        else:
            self.stdout.write(self.style.SUCCESS('Paris location already exists'))

        # Add Country: France (if it doesn't exist)
        france, created = Location.objects.get_or_create(
            id="FR",
            defaults={
                'title': "France",
                'center': Point(2.3522, 48.8566),  # Longitude, Latitude for Paris
                'location_type': "country",
                'country_code': "FR"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('France location created'))
        else:
            self.stdout.write(self.style.SUCCESS('France location already exists'))
