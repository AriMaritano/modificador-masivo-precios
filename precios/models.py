from django.db import models
from datetime import datetime
from django.conf import settings

class File(models.Model):
    file = models.FileField(upload_to=settings.MEDIA_ROOT)
    filename = models.CharField(max_length=200)
    date_uploaded = models.DateTimeField(auto_now_add=True)

