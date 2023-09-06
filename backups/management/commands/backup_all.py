from django.core.management.base import BaseCommand, CommandError

from backups.backup import backup_all

class Command(BaseCommand):
    help = "Backs all postgres database"

    def handle(self, *args, **options):
        backup_all()