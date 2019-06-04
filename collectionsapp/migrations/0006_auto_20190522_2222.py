# Generated by Django 2.2 on 2019-05-23 05:22

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0005_auto_20190517_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottlecap',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]