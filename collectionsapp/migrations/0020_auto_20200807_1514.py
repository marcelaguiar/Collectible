# Generated by Django 3.1 on 2020-08-07 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0019_auto_20200530_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottlecap',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='bottlecap',
            name='image_thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnails/', verbose_name='ImageThumbnail'),
        ),
    ]