from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        
        DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not DJANGO_SUPERUSER_USERNAME or not DJANGO_SUPERUSER_PASSWORD:
            self.stdout.write(self.style.WARNING('Superuser environment variables not set, skipping superuser creation'))
            return
            
        if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
            self.stdout.write(self.style.WARNING(f'Creating superuser {DJANGO_SUPERUSER_USERNAME}'))
            User.objects.create_superuser(
                username=DJANGO_SUPERUSER_USERNAME,
                email=DJANGO_SUPERUSER_EMAIL or '',
                password=DJANGO_SUPERUSER_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {DJANGO_SUPERUSER_USERNAME} already exists'))
