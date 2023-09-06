from django.db import models
from django.utils import timezone


# django model that represents a snapshot
class Snapshot(models.Model):
    database = models.ForeignKey('PostgresDatabase', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self): return f"{self.database} {timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"

class PostgresDatabase(models.Model):
    app_name = models.CharField(max_length=100, unique=True, help_text="The name of the fly app that hosts the database")
    name = models.CharField(max_length=100, help_text="The name of the postgres database")
    host = models.CharField(max_length=100, help_text="Should always be 'localhost' because we run a proxy")
    port = models.IntegerField(help_text="Should always be '5433' because we run a proxy")
    user = models.CharField(max_length=100, help_text="Postgres username")
    password = models.CharField(max_length=100, help_text="Postgres password")

    bucket = models.ForeignKey('S3Bucket', on_delete=models.CASCADE)
    fly_account = models.ForeignKey('FlyAccount', on_delete=models.CASCADE)

    def __str__(self): return self.name

class S3Bucket(models.Model):
    name = models.CharField(max_length=100)
    access_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self): return self.name

class FlyAccount(models.Model):
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    def __str__(self): return self.name
