from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from tasks.models import Location

class Command(BaseCommand):
    help = "Populates initial location data"

    def handle(self, *args, **kwargs):
        Location.objects.bulk_create([
            Location(id="US", title="United States", center=Point(-95.7129, 37.0902), location_type="country"),
            Location(id="CA", title="California", center=Point(-119.4179, 36.7783), location_type="state", parent_id="US"),
            Location(id="LA", title="Los Angeles", center=Point(-118.2437, 34.0522), location_type="city", parent_id="CA"),
        ], ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Locations populated successfully."))
