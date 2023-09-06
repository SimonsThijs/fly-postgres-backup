from django.core.management.base import BaseCommand, CommandError

from backups.backup import backup_loop

class Command(BaseCommand):
    help = "Backs all databases and keep looping"

    def handle(self, *args, **options):
        backup_loop()