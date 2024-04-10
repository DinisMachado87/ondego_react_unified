from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    what_title = models.CharField(max_length=50, blank=True)
    what_content = models.TextField(blank=True)
    where_place = models.CharField(max_length=50, blank=True)
    where_address = models.TextField(max_length=255, blank=True)
    link = models.URLField(max_length=200, blank=True)
    when_start = models.DateTimeField(blank=True, default=timezone.now)
    when_end = models.DateTimeField(blank=True)
    intention = models.TextField(max_length=255, blank=True)

    event_image = models.ImageField(
        upload_to='ondego_events/',
        default='../ondego_event_placeholder/fhq6qy9kir3aw2ngkvlt',
        blank=True
    )

    class Meta:
        ordering = ['-when_start']

    def __str__(self):
        return f'{self.id} {self.title}'
