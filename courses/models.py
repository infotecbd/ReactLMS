from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    enrolled_users = models.ManyToManyField(
        User, related_name='enrolled_courses', blank=True
    )

    def __str__(self):
        return self.title 