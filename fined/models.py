from django.db import models
from django.urls import reverse


class Course(models.Model):
    c_id=models.IntegerField
    title=models.CharField(max_length=255)
    image=models.ImageField(upload_to="photos/%Y/%m/%d/")
    content=models.TextField(blank=True)
    author=models.TextField(blank=True)
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)