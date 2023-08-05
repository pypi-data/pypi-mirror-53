from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter


User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all user devices (and jwts)'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['username']:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError('User "%s" does not exist' % username)

            adapter = get_adapter()
            devices_count = user.devices.count()
            deleted_devices_count = adapter.remove_all_user_devices(user)

            self.stdout.write(self.style.SUCCESS('Deleted {0}/{1} user devices for "{2}"'.format(devices_count, deleted_devices_count, username)))
