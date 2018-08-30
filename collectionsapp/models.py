from datetime import date
from django.contrib.auth.models import User
from django.db import models


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')

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


class BottleCapIcon(CommonInfo):
    name = models.CharField(max_length=50)


class BottleCap(CommonInfo):
    collection_id = models.ForeignKey('Collection', on_delete=models.PROTECT, verbose_name='Collection ID')
    company = models.CharField(max_length=100, blank=True, verbose_name='Company')
    brand = models.CharField(max_length=100, blank=True, verbose_name='Brand')
    product = models.CharField(max_length=100, blank=True, verbose_name='Product')
    flavor = models.CharField(max_length=100, blank=True, verbose_name='Flavor')
    color = models.IntegerField(default=None, blank=True, null=True, verbose_name='Color')

    NONE_SELECTED = 0
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

    beverage_type = models.IntegerField(choices=BEVERAGE_TYPE_CHOICES, default=NONE_SELECTED,
                                        verbose_name='Beverage Type')
    text = models.CharField(max_length=200, blank=True, verbose_name='Text')
    underside = models.CharField(max_length=50, blank=True, verbose_name='Underside')

    date_acquired = models.DateField(default=date.today, verbose_name='Date Acquired')

    DONATED = 1
    PURCHASED = 2
    TRADED = 3
    FOUND = 4

    METHOD_ACQUIRED_CHOICES = (
        (NONE_SELECTED, ''),
        (DONATED, 'Donated'),
        (PURCHASED, 'Purchased'),
        (TRADED, 'Traded'),
        (FOUND, 'Found')
    )

    method_acquired = models.IntegerField(choices=METHOD_ACQUIRED_CHOICES, default=NONE_SELECTED,
                                          verbose_name='Method Acquired')
    spares_available = models.BooleanField(default=False, verbose_name='Spares Available')
    icons = models.ManyToManyField(BottleCapIcon, verbose_name='Icons')
    image = models.ImageField(blank=True, verbose_name='Image')

    def __str__(self):
        return self.brand + ' ' + self.product + ' ' + self.flavor



