from django.contrib import admin
from custom_admin import models


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'deleted_at')
    fields = ('name', 'owner')


class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'admin', 'created_at', 'deleted_at')
    fields = ('name', 'admin', 'institution')


admin.site.register(models.Institution, InstitutionAdmin)
admin.site.register(models.Campus, CampusAdmin)