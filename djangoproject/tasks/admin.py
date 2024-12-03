from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .models import Location, Accommodation, LocalizeAccommodation
from leaflet.admin import LeafletGeoAdmin

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "title",
        "location_type",
        "country_code",
        "state_abbr",
        "city",
    )
    list_filter = ("location_type", "country_code")
    search_fields = ("title", "city", "state_abbr", "country_code")

    # Leaflet map customization options
    default_zoom = 12  # Set the default zoom level for the map
    map_options = {
        'scrollWheelZoom': False,  # Disable scroll wheel zoom for better UI
        'center': [0, 0],  # You can set a default center (lat, long), for example [0, 0]
        'zoom': 12,  # Set the initial zoom level for the map
    }

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
        if (
            request.user.groups.filter(name="Property Owners").exists()
            and request.user.is_active
        ):
            return queryset.filter(user=request.user)  # Filter for Property Owners
        return queryset  # Return all accommodations for admin users

    # Leaflet map customization options
    default_zoom = 12
    map_options = {
        'scrollWheelZoom': False,
        'center': [0, 0],
        'zoom': 12,
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].widget.attrs['disabled'] = 'disabled'
            form.base_fields['user'].required = False
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


# Add Property Owners Group in Admin Interface
class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:  # If creating a new user
            group, _ = Group.objects.get_or_create(name="Property Owners")
            obj.groups.add(group)
            obj.is_active = (
                False  # Initially, set the user as inactive until admin approval
            )
        else:
            # If the user is approved (is_active = True), they can access their accommodations
            if obj.is_active:
                group, _ = Group.objects.get_or_create(name="Property Owners")
                obj.groups.add(group)

        obj.save()  # Save the user model changes


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
