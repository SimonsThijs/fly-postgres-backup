# Generated by Django 4.2.4 on 2023-08-09 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0006_flyaccount_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgresdatabase',
            name='app_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
