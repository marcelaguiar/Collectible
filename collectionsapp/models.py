from datetime import date
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


UNKNOWN_USER_ID = 11


def get_unknown_user():
    return User.objects.get(id=UNKNOWN_USER_ID).pk


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=get_unknown_user,
                                   related_name='%(app_label)s_%(class)s_created', verbose_name='Created By')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, default=get_unknown_user,
                                    related_name='%(app_label)s_%(class)s_modified', verbose_name='Modified By')

    class Meta:
        abstract = True


class CollectionItem(CommonInfo):
    NONE_SELECTED = 0
    DONATED = 1
    PURCHASED = 2
    TRADED = 3
    FOUND = 4
    CREATED = 5

    METHOD_ACQUIRED_CHOICES = (
        (NONE_SELECTED, ''),
        (DONATED, 'Donated'),
        (PURCHASED, 'Purchased'),
        (TRADED, 'Traded'),
        (FOUND, 'Found'),
        (CREATED, 'Created')
    )

    date_acquired = models.DateField(default=date.today, verbose_name='Date Acquired')
    method_acquired = models.IntegerField(choices=METHOD_ACQUIRED_CHOICES, default=NONE_SELECTED,
                                          verbose_name='Method Acquired')
    available_for_trade = models.BooleanField(default=False, verbose_name='Available For Trade')
    image = models.ImageField(blank=True, verbose_name='Image')
    number_in_collection = models.IntegerField(verbose_name='Number in collection')
    tags = TaggableManager(verbose_name='Tags')
    description = models.CharField(max_length=512, blank=True, verbose_name='Description')
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT, verbose_name='Collection ID')

    class Meta:
        abstract = True


class CollectionType(CommonInfo):
    name = models.CharField(max_length=100)
    view_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Collection(CommonInfo):
    name = models.CharField(max_length=100)
    collection_type = models.ForeignKey('CollectionType', on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default=get_unknown_user,
                              related_name='%(app_label)s_%(class)s_owned')

    def __str__(self):
        return self.name


class BottleCap(CollectionItem):
    company = models.CharField(max_length=100, blank=True, verbose_name='Company')
    brand = models.CharField(max_length=100, blank=True, verbose_name='Brand')
    product = models.CharField(max_length=100, blank=True, verbose_name='Product')
    variety = models.CharField(max_length=100, blank=True, verbose_name='Variety')
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

    def __str__(self):
        return self.brand + ' ' + self.product + ' ' + self.variety


class EAVTable(CollectionItem):
    field1Name = models.CharField(max_length=100)
    field1Type = models.CharField(max_length=100)
    field1Value = models.CharField(max_length=200)
