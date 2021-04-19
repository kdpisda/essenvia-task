from django.contrib import admin
from core import models as core_models

# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at', 'updated_at']

    list_filter = ('status',)

admin.site.register(core_models.Data, DataAdmin)