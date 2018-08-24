from datetime import date
from django.contrib.auth.models import User
from django.db import models


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CollectionType(CommonInfo):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Collection(CommonInfo):
    name = models.CharField(max_length=100)
    collection_type_id = models.ForeignKey('CollectionType', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class BottleCap(CommonInfo):
    collection_id = models.ForeignKey('Collection', on_delete=models.PROTECT)
    manufacturer = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    color = models.IntegerField
    date_acquired = models.DateField(default=date.today)

    NONE_SELECTED = 0

    DONATED = 1
    PURCHASED = 2
    TRADED = 3

    METHOD_ACQUIRED_CHOICES = (
        (NONE_SELECTED, ''),
        (DONATED, 'Donated'),
        (PURCHASED, 'Purchased'),
        (TRADED, 'Traded')
    )

    method_acquired = models.IntegerField(choices=METHOD_ACQUIRED_CHOICES, default=NONE_SELECTED)

    SODA = 1
    BEER = 2
    WATER = 3
    MILK = 4
    KOMBUCHA = 5

    BEVERAGE_TYPE_CHOICES = (
        (NONE_SELECTED, ''),
        (SODA, 'Soda'),
        (BEER, 'Beer'),
        (WATER, 'Water'),
        (MILK, 'Milk'),
        (KOMBUCHA, 'Kombucha')
    )

    beverage_type = models.IntegerField(choices=BEVERAGE_TYPE_CHOICES, default=NONE_SELECTED)
    spares_available = models.BooleanField(default=False)
    text = models.CharField(max_length=200, blank=True)
    underside = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.manufacturer + ' ' + self.variety


class BottleCapIcon(CommonInfo):
    name = models.CharField(max_length=50)
    bottle_cap = models.ManyToManyField(BottleCap)
