# Generated by Django 2.2.4 on 2019-08-25 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collectionsapp', '0011_auto_20190824_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottlecap',
            name='beverage_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collectionsapp.BeverageType', verbose_name='Beverage Type'),
        ),
        migrations.AlterField(
            model_name='bottlecap',
            name='method_acquired',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collectionsapp.MethodAcquired', verbose_name='Method Acquired'),
        ),
    ]
