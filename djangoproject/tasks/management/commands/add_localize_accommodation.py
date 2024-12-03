from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from tasks.models import Accommodation, Location, LocalizeAccommodation
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add localizations for accommodations'

    def handle(self, *args, **kwargs):
        # Fetch or create Accommodation
        accommodation, created = Accommodation.objects.get_or_create(
            id="USA-Hotel-01",  # Example accommodation ID
            defaults={
                'title': "Grand Hotel California",
                'country_code': "US",
                'bedroom_count': 5,
                'review_score': 4.5,
                'usd_rate': 250.00,
                'center': Point(-118.2500, 34.0500),
                'published': True,
                'location': Location.objects.get(id="CA"),  # Ensure Location is imported
                'images': ["https://example.com/hotel1.jpg", "https://example.com/hotel2.jpg"],
                'amenities': ["Wi-Fi", "Air conditioning", "Pool", "Gym"]
            }
        )

        # Example 1: Add English Localization
        LocalizeAccommodation.objects.create(
            property=accommodation,
            language="en",  # English language
            description="The Grand Hotel California offers a luxurious stay in the heart of California.",
            policy={"pet_policy": "Pets are not allowed."},
        )

        # Example 2: Add French Localization
        LocalizeAccommodation.objects.create(
            property=accommodation,
            language="fr",  # French language
            description="L'hôtel Grand California offre un séjour luxueux au cœur de la Californie.",
            policy={"pet_policy": "Les animaux ne sont pas autorisés."},
        )

        self.stdout.write(self.style.SUCCESS('Successfully added localizations'))
