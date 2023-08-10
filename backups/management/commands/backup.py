from django.core.management.base import BaseCommand, CommandError

from backups.backup import backup_by_db_name
from backups.models import PostgresDatabase

class Command(BaseCommand):
    help = "Backs up a postgres database"

    def add_arguments(self, parser):
        parser.add_argument("database_name", nargs="+", type=str)

    def handle(self, *args, **options):
        for database_name in options["database_name"]:
            backup_by_db_name(database_name)