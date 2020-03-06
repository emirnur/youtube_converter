from django.db import models


class Download(models.Model):
    url = models.URLField(max_length=128)
    email = models.EmailField(max_length=128)
