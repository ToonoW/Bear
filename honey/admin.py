from django.contrib import admin

from honey import models


@admin.register(models.Honeycomb)
class HoneycombAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'remaining_amount', 'is_checkin', 'last_modify')


@admin.register(models.Honey)
class HoneyAdmin(admin.ModelAdmin):
    pass