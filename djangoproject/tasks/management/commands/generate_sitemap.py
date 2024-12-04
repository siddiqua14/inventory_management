import json
from django.core.management.base import BaseCommand
from tasks.models import Location


class Command(BaseCommand):
    help = 'Generate a sitemap.json file for all locations'

    def handle(self, *args, **kwargs):
        # Fetch all locations with related parent data
        locations = Location.objects.select_related('parent').all()

        # Dictionary to store country-level data
        country_data = {}

        # Process each location
        for location in locations:
            # Handle country
            if location.location_type == 'country':
                country_slug = location.title.lower().replace(" ", "-")
                if country_slug not in country_data:
                    country_data[country_slug] = {
                        'title': location.title,
                        'slug': country_slug,
                        'locations': []
                    }

            # Handle state
            elif location.location_type == 'state' and location.parent:
                parent_country_slug = location.parent.title.lower().replace(" ", "-")
                if parent_country_slug in country_data:
                    country = country_data[parent_country_slug]
                    state_slug = location.title.lower().replace(" ", "-")
                    # Check if the state already exists
                    state_entry = next(
                        (state for state in country['locations'] if state['slug'] == state_slug), None
                    )
                    if not state_entry:
                        state_entry = {
                            'title': location.title,
                            'slug': state_slug,
                            'url': f"{location.parent.country_code.lower()}/{state_slug}",
                            'locations': []
                        }
                        country['locations'].append(state_entry)

            # Handle city
            elif location.location_type == 'city' and location.parent:
                parent_location = location.parent
                city_slug = location.title.lower().replace(" ", "-")
                if parent_location.location_type == 'state' and parent_location.parent:
                    parent_country_slug = parent_location.parent.title.lower().replace(" ", "-")
                    if parent_country_slug in country_data:
                        country = country_data[parent_country_slug]
                        state_slug = parent_location.title.lower().replace(" ", "-")
                        # Find the parent state under the country
                        state_entry = next(
                            (state for state in country['locations'] if state['slug'] == state_slug), None
                        )
                        if state_entry:
                            # Add city under the state
                            city_entry = next(
                                (city for city in state_entry['locations'] if city['slug'] == city_slug), None
                            )
                            if not city_entry:
                                state_entry['locations'].append({
                                    'title': location.title,
                                    'slug': city_slug,
                                    'url': f"{parent_location.parent.country_code.lower()}/{state_slug}/{city_slug}"
                                })
                elif parent_location.location_type == 'country':
                    # Add city directly under the country if no state exists
                    parent_country_slug = parent_location.title.lower().replace(" ", "-")
                    if parent_country_slug in country_data:
                        country = country_data[parent_country_slug]
                        city_entry = next(
                            (city for city in country['locations'] if city['slug'] == city_slug), None
                        )
                        if not city_entry:
                            country['locations'].append({
                                'title': location.title,
                                'slug': city_slug,
                                'url': f"{parent_location.country_code.lower()}/{city_slug}"
                            })

        # Convert dictionary to a list
        sitemap = list(country_data.values())

        # Write the sitemap to a JSON file
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=2)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
