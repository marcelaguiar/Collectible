# Generated by Django 2.2 on 2019-05-18 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0004_remove_bottlecap_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottlecap',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collectionsapp.Collection', verbose_name='Collection'),
        ),
    ]
