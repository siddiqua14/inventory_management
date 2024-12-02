import json
from django.core.management.base import BaseCommand
from tasks.models import Location

class Command(BaseCommand):
    help = 'Generate a sitemap.json file for all country locations'

    def handle(self, *args, **kwargs):
        # Fetch all countries
        countries = Location.objects.filter(location_type='country')

        sitemap = []

        for country in countries:
            country_data = {
                country.title: country.country_code.lower(),
                "locations": []
            }

            # Find the states under the country
            states = Location.objects.filter(parent=country)

            for state in states:
                state_data = {
                    state.title: f"{country.country_code.lower()}/{state.state_abbr.lower()}"
                }
                state_data["locations"] = []

                # Find cities under the state
                cities = Location.objects.filter(parent=state)
                for city in cities:
                    state_data["locations"].append({
                        city.title: f"{country.country_code.lower()}/{state.state_abbr.lower()}/{city.id.lower()}"
                    })

                country_data["locations"].append(state_data)

            # Add the country data to the sitemap
            sitemap.append(country_data)

        # Write the sitemap to a file
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=2)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
