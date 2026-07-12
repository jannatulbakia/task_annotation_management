from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the admin user"

    def handle(self, *args, **kwargs):
        email = "admin@gmail.com"
        password = "Admin123!"
        username = "admin"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if not created:
            user.username = username
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Admin created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("Admin updated successfully."))