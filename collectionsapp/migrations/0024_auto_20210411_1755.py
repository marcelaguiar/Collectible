# Generated by Django 3.1 on 2021-04-12 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0023_bottlecap_image_thumbnail_tiny'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bottlecap',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='bottlecap',
            name='method_acquired',
        ),
        migrations.DeleteModel(
            name='MethodAcquired',
        ),
    ]