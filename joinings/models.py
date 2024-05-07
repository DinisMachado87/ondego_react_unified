from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Joining(models.Model):
    """
    Joining model. A Joining is a user joining an event.
    """
    joining_choices = [
        (1, 'Cannot'),
        (2, 'Joining'),
        (3, 'let me see'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='joining')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    joining_status = models.IntegerField(
        choices=joining_choices,
        default=1
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'event']

    def __str__(self):
        return f'{self.owner} {self.joining_status} {self.event} at {self.updated_at}'
