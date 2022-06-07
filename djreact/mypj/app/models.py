from django.db import models
# Create your models here.
class MatchImage(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)