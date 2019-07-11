from datetime import date
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='%(app_label)s_%(class)s_created', verbose_name='Created By')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='%(app_label)s_%(class)s_modified', verbose_name='Modified By')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CollectionItem(CommonInfo):
    date_acquired = models.DateField(default=date.today, verbose_name='Date Acquired')
    method_acquired = models.ForeignKey('MethodAcquired', on_delete=models.PROTECT, verbose_name="Method Acquired")
    available_for_trade = models.BooleanField(default=False, verbose_name='Available For Trade')
    tags = TaggableManager(verbose_name='Tags', blank=True)
    description = models.CharField(max_length=512, blank=True, verbose_name='Description')
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT, verbose_name='Collection')

    class Meta:
        abstract = True


class CollectionType(CommonInfo):
    name = models.CharField(max_length=100, verbose_name="Name")

    def __str__(self):
        return self.name


class Collection(CommonInfo):
    name = models.CharField(max_length=100, verbose_name="Name")
    type = models.ForeignKey('CollectionType', on_delete=models.PROTECT, verbose_name="Collection Type")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_owned',
                              verbose_name="Owner")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='owner cannot repeat collection names')
        ]


class CollectionItemImage(CommonInfo):
    image = models.ImageField(verbose_name='Image', upload_to='images/')
    collection_item = models.ForeignKey('BottleCap', on_delete=models.PROTECT, verbose_name='Collection Item')
    order_in_collection = models.PositiveSmallIntegerField(verbose_name='Order', default=1)


class CollectionItemImageThumbnail(CommonInfo):
    image = models.ImageField(verbose_name='Image', upload_to='thumbnails/')
    collection_item = models.ForeignKey('BottleCap', on_delete=models.PROTECT, verbose_name='Collection Item')
    order_in_collection = models.PositiveSmallIntegerField(verbose_name='Order', default=1)


class BottleCap(CollectionItem):
    company = models.CharField(max_length=100, blank=True, verbose_name='Company')
    brand = models.CharField(max_length=100, blank=True, verbose_name='Brand')
    product = models.CharField(max_length=100, blank=True, verbose_name='Product')
    variety = models.CharField(max_length=100, blank=True, verbose_name='Variety')
    beverage_type = models.ForeignKey('BeverageType', on_delete=models.PROTECT, verbose_name="Beverage Type")
    text = models.CharField(max_length=200, blank=True, verbose_name='Text')
    underside = models.CharField(max_length=50, blank=True, verbose_name='Underside')

    def __str__(self):
        strings = [self.brand, self.product, self.variety]
        return ' - '.join(filter(None, strings))


class BeverageType(CommonInfo):
    name = models.CharField(max_length=100, blank=False, verbose_name='Beverage type')

    def __str__(self):
        return self.name


class MethodAcquired(CommonInfo):
    name = models.CharField(max_length=100, blank=False, verbose_name='Method acquired')

    def __str__(self):
        return self.name
