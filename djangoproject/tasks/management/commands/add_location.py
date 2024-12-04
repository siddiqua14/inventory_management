from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Add locations to the database'

    def handle(self, *args, **kwargs):
        # Get the Location model dynamically from the app registry
        Location = apps.get_model('tasks', 'Location')

        # Add Country: India
        india, created = Location.objects.get_or_create(
            id=1,  # Use integer ID for India
            defaults={
                'title': "India",
                'center': Point(78.9629, 20.5937),  # Longitude, Latitude for India
                'location_type': "country",
                'country_code': "IN"
            }
        )
        if not created:
            india.title = "India"
            india.center = Point(78.9629, 20.5937)
            india.location_type = "country"
            india.country_code = "IN"
            india.save()

        # Add State: Maharashtra
        maharashtra, created = Location.objects.get_or_create(
            id=2,
            defaults={
                'title': "Maharashtra",
                'center': Point(19.2183, 72.9787),
                'location_type': "state",
                'state_abbr': "MH",
                'country_code': "IN",
            }
        )
        maharashtra.parent = india  # Explicitly set the parent
        maharashtra.save()

        # Add City: Mumbai
        mumbai, created = Location.objects.get_or_create(
            id=3,
            defaults={
                'title': "Mumbai",
                'center': Point(72.8777, 19.0760),
                'location_type': "city",
                'country_code': "IN",
                'state_abbr': "MH",
                'city': "Mumbai",
            }
        )
        mumbai.parent = maharashtra  # Explicitly set the parent
        mumbai.save()

        # Other locations (e.g., US, France) follow a similar pattern

        # Add Country: United States
        us, created = Location.objects.get_or_create(
            id=4,
            defaults={
                'title': "United States",
                'center': Point(-99.9018, 37.0902),
                'location_type': "country",
                'country_code': "US"
            }
        )
        if not created:
            us.title = "United States"
            us.center = Point(-99.9018, 37.0902)
            us.location_type = "country"
            us.country_code = "US"
            us.save()

        # Add State: California
        california, created = Location.objects.get_or_create(
            id=5,
            defaults={
                'title': "California",
                'center': Point(-119.4179, 36.7783),
                'location_type': "state",
                'state_abbr': "CA",
                'country_code': "US",
            }
        )
        california.parent = us  # Explicitly set the parent
        california.save()

        # Add City: Los Angeles
        los_angeles, created = Location.objects.get_or_create(
            id=6,
            defaults={
                'title': "Los Angeles",
                'center': Point(-118.2437, 34.0522),
                'location_type': "city",
                'country_code': "US",
                'state_abbr': "CA",
                'city': "Los Angeles",
            }
        )
        los_angeles.parent = california  # Explicitly set the parent
        los_angeles.save()
        # Add Country: France
        france, created = Location.objects.get_or_create(
            id=7,
            defaults={
                'title': "France",
                'center': Point(2.2137, 46.2276),  # Longitude, Latitude for France
                'location_type': "country",
                'country_code': "FR"
            }
        )
        if not created:
            france.title = "France"
            france.center = Point(2.2137, 46.2276)
            france.location_type = "country"
            france.country_code = "FR"
            france.save()


        self.stdout.write(self.style.SUCCESS('All locations have been added/updated successfully.'))
