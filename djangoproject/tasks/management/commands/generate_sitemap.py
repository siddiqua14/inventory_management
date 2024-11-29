import json
from django.core.management.base import BaseCommand
from tasks.models import Location

class Command(BaseCommand):
    help = 'Generate a sitemap.json file for all country locations'

    def handle(self, *args, **kwargs):
        countries = Location.objects.filter(location_type='country')

        sitemap = []

        for country in countries:
            country_data = {
                country.title: country.id.lower(),
                "locations": []
            }
            states = Location.objects.filter(parent=country)

            for state in states:
                country_data["locations"].append({
                    state.title: f"{country.id.lower()}/{state.id.lower()}"
                })

            sitemap.append(country_data)

        # Write the sitemap to a file
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=2)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
