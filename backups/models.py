from django.db import models
from django.utils import timezone


# django model that represents a snapshot
class Snapshot(models.Model):
    database = models.ForeignKey('PostgresDatabase', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self): return f"{self.database} {timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"

class PostgresDatabase(models.Model):
    app_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

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
