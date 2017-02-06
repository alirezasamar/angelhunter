from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ListSector(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'list_selection'

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class TypeSector(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'type_selection'

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class LocationSector(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'location_selection'

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class MarketSector(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'market_selection'

    def __str__(self):              # __unicode__ on Python 2
        return self.name



class StageSector(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'stage_selection'

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Selection(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'selection_types'

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Schedular(models.Model):
    query = models.CharField(max_length=255, default=None, blank=True, null=True)
    lists = models.ForeignKey(ListSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    types = models.ForeignKey(TypeSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(LocationSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    market = models.ForeignKey(MarketSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    stage = models.ForeignKey(StageSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    schedule_date = models.DateTimeField()
    selection = models.ForeignKey(Selection, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class CompaniesData(models.Model):
    name = models.CharField(max_length=255, default=None, blank=True, null=True)
    description = models.CharField(max_length=255, default=None, blank=True, null=True)
    image_url = models.CharField(max_length=255, default=None, blank=True, null=True)
    joined = models.CharField(max_length=255, default=None, blank=True, null=True)
    location = models.CharField(max_length=255, default=None, blank=True, null=True)
    market = models.CharField(max_length=255, default=None, blank=True, null=True)
    website = models.CharField(max_length=255, default=None, blank=True, null=True)
    employees = models.CharField(max_length=255, default=None, blank=True, null=True)
    stage = models.CharField(max_length=255, default=None, blank=True, null=True)
    total_raised = models.CharField(max_length=255, default=None, blank=True, null=True)
    lists = models.ForeignKey(ListSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    types = models.ForeignKey(TypeSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    locationfil = models.ForeignKey(LocationSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    marketfil = models.ForeignKey(MarketSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    stagefil = models.ForeignKey(StageSector, default=None, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'companies_data'


class PostType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'post_type'

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Angel(models.Model):
    types = models.ForeignKey(PostType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, default=None, blank=True, null=True)
    pic = models.CharField(max_length=255, default=None, blank=True, null=True)
    url = models.CharField(max_length=255, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'angel_data'