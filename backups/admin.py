from django.contrib import admin

from backups.models import PostgresDatabase, S3Bucket, Snapshot, FlyAccount



admin.site.site_header = 'Fly Postgres Backup Admin'


admin.site.register(PostgresDatabase)
admin.site.register(S3Bucket)
admin.site.register(Snapshot)
admin.site.register(FlyAccount)



