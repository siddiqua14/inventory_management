from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tasks.models import Accommodation

class Command(BaseCommand):
    help = "Create initial user groups"

    def handle(self, *args, **kwargs):
        group_name = "Property Owners"
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' created successfully!"))
        else:
            self.stdout.write(f"Group '{group_name}' already exists.")

        # Assign permissions for Property Owners (view, add, and change Accommodation)
        content_type = ContentType.objects.get_for_model(Accommodation)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=["view_accommodation", "add_accommodation", "change_accommodation"])
        
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS(f"Permissions assigned to '{group_name}' group."))
