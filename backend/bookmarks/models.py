from django.db import models
from django.contrib.auth.models import User


class Bookmarks(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500, null=False)
    url = models.CharField(max_length=3000, null=False)
    category = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(
        User, related_name='bookmarks', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.text} by {self.owner}"
