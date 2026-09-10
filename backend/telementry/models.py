from django.db import models
from devices.models import Device

class Telementry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="telementry")
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.name} @ {self.timestamp}"
        