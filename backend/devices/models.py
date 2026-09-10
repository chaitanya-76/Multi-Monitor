import secrets
from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    os_type = models.CharField(max_length=20, default='linux')
    token = models.CharField(max_length=64, unique=True, editable=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)

    @property
    def is_online(self):
        from django.utils import timezone
        if not self.last_seen:
            return False
        return (timezone.now() - self.last_seen).total_seconds() < 30

    def __str__(self):
        return f"{self.name} ({self.owner.username})"