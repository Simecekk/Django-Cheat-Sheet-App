from django.core.management import BaseCommand

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from hollymovies_app.general_permissions import GENERAL_PERMISSIONS


class Command(BaseCommand):
    help = 'Create custom permissions for Hollymovies App'

    def handle(self, *args, **options):
        content_type, _ = ContentType.objects.get_or_create(app_label='dummyApp', model='DummyModel')
        for codename, name in GENERAL_PERMISSIONS.items():
            Permission.objects.create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
