# Generated by Django 4.2.4 on 2023-08-09 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostgresDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('host', models.CharField(max_length=100)),
                ('port', models.IntegerField()),
                ('user', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='S3Bucket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('access_key', models.CharField(max_length=100)),
                ('secret_key', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backups.postgresdatabase')),
            ],
        ),
        migrations.AddField(
            model_name='postgresdatabase',
            name='bucket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backups.s3bucket'),
        ),
    ]
