from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    list_filter = ('location_type', 'country_code')
    search_fields = ('title', 'city', 'state_abbr', 'country_code')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'location', 'published', 'created_at', 'updated_at'
    )
    list_filter = ('country_code', 'location', 'published')
    search_fields = ('title', 'country_code', 'location__title')
    list_editable = ('published',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language', 'description')
    search_fields = ('property__title', 'language')
    list_filter = ('language',)
