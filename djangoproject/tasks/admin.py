from django.contrib import admin
from .models import Location,Accommodation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')
    search_fields = ('title', 'city', 'state_abbr', 'country_code')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'location', 'published', 'created_at', 'updated_at'
    )
    list_filter = ('country_code', 'location', 'published')
    search_fields = ('title', 'country_code', 'location__title')
    list_editable = ('published',)
    readonly_fields = ('created_at', 'updated_at')