# Generated by Django 2.2 on 2019-05-14 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0003_auto_20190513_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bottlecap',
            name='color',
        ),
    ]
