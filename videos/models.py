import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.contrib.auth.models import User
from courses.models import Course, Category


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    enrolled_users = models.ManyToManyField(
        User, related_name='enrolled_video_access', blank=True
    )
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


# ✅ Delete video file when Video object is deleted
@receiver(post_delete, sender=Video)
def delete_video_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        file_path = instance.video_file.path
        if os.path.isfile(file_path):
            os.remove(file_path)


# ✅ Delete old file when replacing with a new one
@receiver(pre_save, sender=Video)
def delete_old_video_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, nothing to delete
    try:
        old_file = Video.objects.get(pk=instance.pk).video_file
    except Video.DoesNotExist:
        return
    new_file = instance.video_file
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
