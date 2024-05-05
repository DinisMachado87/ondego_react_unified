import os
from django.contrib.auth.models import User
from .models import Comment
from events.models import Event
from friends.models import Friend
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class commentsTests(APITestCase):

    def setUp(self):
        # Create users
        self.claudia = User.objects.create_user(
            username='Claudia',
            password='testpassword'
        )
        self.heliot = User.objects.create_user(
            username='Heliot',
            password='testpassword'
        )
        
        self.catarina = User.objects.create_user(
            username='Catarina',
            password='testpassword'
        )

        # Create an event
        Event.objects.create(
            owner=self.claudia,
            what_title='Birthday Party',
            what_content='Come celebrate with me!',
            where_place='123 Main St',
            where_address='123 Main St',
            when_start=timezone.make_aware(
                timezone.datetime(2021, 8, 1, 12, 0)
            ),
            when_end=timezone.make_aware(
                timezone.datetime(2021, 8, 1, 14, 0)
            ),
            intention='Cyborg extravaganza!',
            event_image='image.jpg'
        )

        # Create Claudia's comment
        Comment.objects.create(
            owner=self.claudia,
            event=Event.objects.get(what_title='Birthday Party'),
            message='Happy Birthday!'
        )
        
        # Create Heliot's comment
        Comment.objects.create(
            owner=self.heliot,
            event=Event.objects.get(what_title='Birthday Party'),
            message='Happy Birthday, Claudia!'
        )
        
        # Create mutual friendship instances between Claudia and Heliot
        Friend.objects.create(
            owner=self.claudia,
            friend=self.heliot
        )
        
        Friend.objects.create(
            owner=self.heliot,
            friend=self.claudia
        )

    def test_logged_in_user_can_see_comments_in_events_by_friends(self):
        # Check that a logged in user can see comments in events by friends
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_logged_in_user_can_create_comments_in_events_by_friends(self):
        # Check that a logged in user can create comments in events by friends
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/comments/',
            {
                'owner': self.claudia.id,
                'event': Event.objects.get(what_title='Birthday Party').id,
                'message': 'Happy Birthday, Heliot!'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Happy Birthday, Heliot!')
        
    def test_logged_in_user_can_delete_own_comments_in_events_by_friends(self):
        # Check that a logged in user can delete own comments in events by friends
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_logged_in_user_cannot_delete_other_comments_in_events_by_friends(self):
        # Check that a logged in user cannot delete other comments in events by friends
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.delete('/comments/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
