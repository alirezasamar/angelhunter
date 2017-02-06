from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.models import User, Group

class SchedularData(admin.ModelAdmin):
    list_display = ('query', 'lists', 'types', 'location', 'market', 'schedule_date', 'created_at', 'selection')
    list_per_page = 20
    list_filter = ('selection', )

class AuthAngel(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url', 'joined', 'location', 'market', 'website', 'employees', 'stage', 'total_raised', 'created_at')
    list_per_page = 20

    fields = ('name', 'description', 'image_url', 'joined', 'location', 'market', 'website', 'employees', 'stage', 'total_raised')

    list_filter = ('lists', 'types', 'locationfil', 'marketfil', 'stagefil')


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(ListSector)
admin.site.register(TypeSector)
admin.site.register(LocationSector)
admin.site.register(MarketSector)
admin.site.register(StageSector)
admin.site.register(Schedular, SchedularData)
admin.site.register(CompaniesData, AuthAngel)