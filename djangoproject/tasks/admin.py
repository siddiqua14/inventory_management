from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .models import Location, Accommodation, LocalizeAccommodation
from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ExportMixin, ImportExportMixin
from import_export import resources
from django.contrib.gis.geos import Point


# Define the resource for the Location model
class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = (
            "id",
            "title",
            "location_type",
            "country_code",
            "state_abbr",
            "city",
            "center",
        )

    def before_import_row(self, row, **kwargs):
        if "center" in row and row["center"]:
            try:
                lng, lat = map(
                    float, row["center"].replace("POINT(", "").replace(")", "").split()
                )
                row["center"] = Point(lng, lat, srid=4326)
            except ValueError as e:
                row["center"] = None


# Add ImportExportMixin to enable import/export functionality
@admin.register(Location)
class LocationAdmin(ImportExportMixin, LeafletGeoAdmin):
    resource_class = LocationResource
    list_display = (
        "id",
        "title",
        "location_type",
        "country_code",
        "state_abbr",
        "city",
        "created_at",
        "updated_at",
    )
    list_filter = ("location_type", "country_code")
    search_fields = ("title", "city", "state_abbr", "country_code")
    default_zoom = 12
    map_options = {
        "scrollWheelZoom": False,
        "center": [0, 0],
        "zoom": 12,
    }
    ordering = ('id',) 


@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "title",
        "country_code",
        "bedroom_count",
        "review_score",
        "usd_rate",
        "location",
        "published",
        "created_at",
        "updated_at",
    )
    list_filter = ("country_code", "location", "published")
    search_fields = ("title", "country_code", "location__title")
    list_editable = ("published",)
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name="Property Owners").exists():
            return queryset.filter(user=request.user)  # Filter for Property Owners
        return queryset # Return all accommodations for admin users

    # Leaflet map customization options
    default_zoom = 12
    map_options = {
        "scrollWheelZoom": False,
        "center": [0, 0],
        "zoom": 12,
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["user"].widget.attrs["disabled"] = "disabled"
            form.base_fields["user"].required = False
        return form

    def save_model(self, request, obj, form, change):
        # Auto-update the country code based on the location
        location = obj.location

        if location and location.country_code:
            obj.country_code = location.country_code

        super().save_model(request, obj, form, change)


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "language", "description")
    search_fields = ("property__title", "language")
    list_filter = ("language",)


