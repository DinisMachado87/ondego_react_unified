from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class FriendRequest(models.Model):
    '''
    FriendRequest model. 
    Intermidiary instance between two users to request friendship.
    '''
    owner = models.ForeignKey(
        User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='received_requests', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'to_user']

    def __str__(self):
        return f'{self.owner} requested {self.to_user}'

    @staticmethod
    def get_friend_requests(user):
        '''
        Get all friend requests for a user
        '''
        return FriendRequest.objects.filter(to_user=user)


class Friend(models.Model):
    '''
    Friend model. A Friend is a user's friend.
    '''
    owner = models.ForeignKey(
        User, related_name='user_friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, related_name='friend_friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'friend']

    def __str__(self):
        return f'{self.owner} is friends with {self.friend}'


@receiver(post_save, sender=FriendRequest)
def handle_friend_request(sender, instance, created, **kwargs):
    '''
    When a FriendRequest is approved, create Friend instances for both users
    '''
    if instance.is_approved and created:
        # Create Friend instance for the sender (from_user)
        Friend.objects.create(
            owner=instance.from_user, friend=instance.to_user)

        # Create Friend instance for the receiver (to_user)
        Friend.objects.create(
            owner=instance.to_user, friend=instance.from_user)

        # Delete the friend request
        instance.delete()


@receiver(pre_delete, sender=Friend)
def handle_friend_deletion(sender, instance, **kwargs):
    '''
    When a Friend instance is deleted, delete the corresponding Friend instance
    '''
    # Get the corresponding friend instance for the other user
    try:
        corresponding_friend = Friend.objects.get(
            owner=instance.friend, friend=instance.owner)
        corresponding_friend.delete()
    except Friend.DoesNotExist:
        # Corresponding friend instance does not exist, no action needed
        pass
