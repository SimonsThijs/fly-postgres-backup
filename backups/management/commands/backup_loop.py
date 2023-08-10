from django.core.management.base import BaseCommand, CommandError

from backups.backup import backup_loop

class Command(BaseCommand):
    help = "Backs up a postgres database"

    def handle(self, *args, **options):
        backup_loop()