from django.conf import settings
from django.utils import timezone

from backups.models import Snapshot, PostgresDatabase, S3Bucket

import time
from datetime import datetime
import os

from rich import print as rprint
import sh
import boto3


class Proxy():
    def __init__(self, fly_secret: str, app_name: str, port: int = 5433, bg: int = 1):
        self.fly_secret = fly_secret
        self.app_name = app_name
        self.port = port
        self.bg = bg
        self.connection = None

    def __enter__(self):
        self.connection = sh.fly("proxy", f"{self.port}:5432", app=self.app_name, access_token=self.fly_secret, _out=rprint, _bg=self.bg)
        time.sleep(3)
        return self

    def __exit__(self, type, value, traceback):
        if not self.connection is None:
            self.connection.terminate()


def fly_db_backup(
    fly_secret,
    password=None,
    db_name="db",
    port=5433,
    user="postgres",
    host="localhost",
    app_name="app-name",
):
    """Connect to fly.io and backup the database"""

    proxy = Proxy(fly_secret=fly_secret, app_name=app_name, port=port, bg=1)
    with proxy as p:
        
        # start timer
        start = time.time()

        filename = os.path.join(settings.BASE_DIR, "tmp", "tmp.sql")

        process = sh.pg_dump(
            "-h",
            host,
            "-p",
            port,
            "-U",
            user,
            "-f",
            filename,
            db_name,
            _out=rprint,
            _in=password,
            _bg=False,
        )
        rprint(process)

        # end timer
        end = time.time()

        
    return filename


def upload_file(file_name, s3_filename, bucket_name, access_key, secret_key, region):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """


    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    s3_client.upload_file(file_name, bucket_name, s3_filename)


def backup(db: PostgresDatabase):
    """
    Backup a single database
    """

    now = timezone.now()

    filename = fly_db_backup(fly_secret=db.fly_account.secret, password=db.password, db_name=db.name, host=db.host, port=db.port, user=db.user, 
                            app_name=db.app_name)
    
    bucket = db.bucket
    s3_filename = f"{db.name}/{now.strftime('%Y-%m-%d-%H-%M-%S')}.sql"
    upload_file(filename, s3_filename, bucket.name, bucket.access_key, bucket.secret_key, bucket.region)

    sh.rm(filename)

    # create a snapshot
    snapshot = Snapshot(database=db, created_at=now)
    snapshot.save()


def backup_by_db_name(name: str):
    """
    Backup a single database by name
    """
    db = PostgresDatabase.objects.get(name=name)
    backup(db)


def backup_all():
    for db in PostgresDatabase.objects.all():
        time.sleep(3)
        try:
            backup(db)
        except Exception as e:
            rprint(f"[red]Error backing up {db.name}:\n{e}")


def backup_loop():
    """
    Backup all databases in a loop
    """
    while True:
        backup_all()
        # sleep 1 hour
        time.sleep(60 * 60)