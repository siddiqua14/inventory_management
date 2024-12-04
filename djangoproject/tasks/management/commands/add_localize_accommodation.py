from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from tasks.models import Location, Accommodation, LocalizeAccommodation
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Add localizations for accommodations"

    def handle(self, *args, **kwargs):
        # Fetch Accommodation entries (you can adjust the logic to fetch specific ones)
        accommodations = Accommodation.objects.all()

        if not accommodations:
            self.stdout.write(
                self.style.ERROR("No accommodations found in the database")
            )
            return

        # Loop through accommodations and create localizations
        for accommodation in accommodations:
            # Example: Add English localization
            self.add_localization(
                accommodation,
                "en",
                "The Grand Hotel California offers a luxurious stay in the heart of California.",
                {"pet_policy": "Pets are not allowed."},
            )

            # Example: Add French localization
            self.add_localization(
                accommodation,
                "fr",
                "L'hôtel Grand California offre un séjour luxueux au cœur de la Californie.",
                {"pet_policy": "Les animaux ne sont pas autorisés."},
            )

        self.stdout.write(self.style.SUCCESS("Successfully added localizations"))

    def add_localization(self, accommodation, language, description, policy):
        # Check if localization exists; if not, create it
        localization, created = LocalizeAccommodation.objects.get_or_create(
            property=accommodation,
            language=language,
            defaults={"description": description, "policy": policy},
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Localization added for {accommodation.title} in {language}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Localization for {accommodation.title} in {language} already exists"
                )
            )
