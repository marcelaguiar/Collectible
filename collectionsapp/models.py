from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from taggit.managers import TaggableManager


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                   related_name='%(app_label)s_%(class)s_created', verbose_name='Created By')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                    related_name='%(app_label)s_%(class)s_modified', verbose_name='Modified By')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CollectionType(CommonInfo):
    name = models.CharField(max_length=100, verbose_name="Name")

    def __str__(self):
        return self.name


class Collection(CommonInfo):
    name = models.CharField(max_length=100, verbose_name="Name")
    type = models.ForeignKey('CollectionType', on_delete=models.PROTECT, verbose_name="Collection Type")
    description = models.TextField(max_length=1000, blank=True, verbose_name="Description")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_owned',
                              verbose_name="Owner")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='owner cannot repeat collection names')
        ]


class CollectionItem(CommonInfo):
    available_for_trade = models.BooleanField(default=False, verbose_name='Available For Trade')
    tags = TaggableManager(verbose_name='Tags', blank=True)
    description = models.CharField(max_length=512, blank=True, verbose_name='Description')
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, verbose_name='Collection')
    image = models.ImageField(verbose_name='Image', upload_to='images/')
    image_thumbnail = models.ImageField(verbose_name='Image Thumbnail', upload_to='thumbnails/')
    image_thumbnail_tiny = models.ImageField(verbose_name='Tiny Image Thumbnail', upload_to='thumbnails_tiny/',
                                             blank=True, null=True)

    class Meta:
        abstract = True


class BottleCap(CollectionItem):
    company = models.CharField(max_length=100, blank=True, verbose_name='Company')
    brand = models.CharField(max_length=100, blank=True, verbose_name='Brand')
    product = models.CharField(max_length=100, blank=True, verbose_name='Product')
    variety = models.CharField(max_length=100, blank=True, verbose_name='Variety')
    beverage_type = models.ForeignKey('BeverageType', on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name="Beverage Type")
    text = models.CharField(max_length=200, blank=True, verbose_name='Text')
    region = models.CharField(max_length=100, blank=True, verbose_name='Region')
    underside = models.CharField(max_length=50, blank=True, verbose_name='Underside')

    def __str__(self):
        strings = [self.brand, self.product, self.variety]
        return ' - '.join(filter(None, strings))


class BeverageType(CommonInfo):
    name = models.CharField(max_length=100, blank=False, verbose_name='Beverage type')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SearchAction(models.Model):
    timestamp = models.DateTimeField(verbose_name='Timestamp')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user', blank=True, null=True,
                             verbose_name='User')
    text = models.CharField(max_length=200, blank=True, verbose_name='Text')

    def __str__(self):
        return str(self.timestamp) + ': \"' + self.text + '\"'


@receiver(signal=models.signals.pre_delete, sender=BottleCap)
def bottlecap_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.image_thumbnail:
        instance.image_thumbnail.delete(save=False)
    if instance.image:
        instance.image.delete(save=False)
