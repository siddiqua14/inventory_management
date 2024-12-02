from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Location(models.Model):
    LOCATION_TYPES = [
        ('continent', 'Continent'),
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    center = gis_models.PointField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    location_type = models.CharField(
        max_length=20, 
        choices=LOCATION_TYPES, 
        null=False, 
        blank=False, 
        default='country'  # Set a default value here
    )
    country_code = models.CharField(max_length=2, blank=True, null=True)
    state_abbr = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100, null=False, blank=False)
    country_code = models.CharField(max_length=2, null=False, blank=False)
    bedroom_count = models.PositiveIntegerField(null=True, blank=True)
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = gis_models.PointField()
    images = models.JSONField(default=list)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    amenities = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)  # Auto incrementing primary key
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='localizations')
    language = models.CharField(max_length=2)  # Language code (e.g., "en" for English, "fr" for French)
    description = models.TextField()  # Localized description
    policy = models.JSONField()  # Store policy in JSONB format, e.g., {"pet_policy": "value"}

    def __str__(self):
        return f"{self.language} localization for {self.property.title}"