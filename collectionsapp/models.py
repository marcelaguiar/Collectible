from django.db import models

# Create your models here.
class Collection(models.Model):
    collection_type_id = models.ForeignKey('CollectionType', on_delete=models.PROTECT)


class CollectionType(models.Model):
    name = models.CharField(max_length=200)


class BottleCap(models.Model):
    manufacturer = models.CharField(max_length=200)
