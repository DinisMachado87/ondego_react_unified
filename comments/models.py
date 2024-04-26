from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Comment(models.Model):
    """
    Comment model. A Comment is a message added by a user to an event's chat.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message
