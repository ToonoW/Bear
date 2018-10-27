from django.contrib import admin

from honey import models


@admin.register(models.Honeycomb)
class HoneycombAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Honey)
class HoneyAdmin(admin.ModelAdmin):
    pass