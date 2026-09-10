from django.contrib import admin
from .models import Device

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ['token']
    list_display = ['name', 'owner', 'os_type', 'is_online', 'last_seen']

admin.site.register(Device, DeviceAdmin)