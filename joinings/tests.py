from django.contrib.auth.models import User
from joinings.models import Joining
from events.models import Event
from friends.models import Friend
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone


class JoiningTests(APITestCase):
    def setUp(self):
        '''
        Create three users, two are friends, and create an event, and comments.
        '''
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

        # Create Friend objects
        Friend.objects.create(
            owner=self.claudia,
            friend=self.heliot
        )
        Friend.objects.create(
            owner=self.heliot,
            friend=self.claudia
        )

    def test_logged_in_user_can_create_joining(self):
        '''
        Check if a logged in user can create a joining.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/joinings/',
            {
                'event': 1,
                'joining_status': '2'
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['event'], 1)
        self.assertEqual(response.data['owner'], self.claudia.username)

    def test_logged_in_user_can_change_joining_status(self):
        '''
        Check if a logged in user can change the joining status.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/joinings/',
            {
                'event': 1,
                'joining_status': '2'
            },
        )

        # Change the joining status
        response = self.client.put(
            '/joinings/1/',
            {
                'event': 1,
                'joining_status': '3'
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['joining_status'], 3)

    def test_other_user_cannot_change_joining_status(self):
        '''
        Check if a user cannot change the joining status of another user.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/joinings/',
            {
                'event': 1,
                'joining_status': '2'
            },
        )
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.put(
            '/joinings/1/',
            {
                'event': 1,
                'joining_status': '3'
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.')

    def test_logged_in_user_can_delete_joining(self):
        '''
        Check if a logged in user can delete a joining.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/joinings/',
            {
                'event': 1,
                'joining_status': '2'
            },
        )
        response = self.client.delete('/joinings/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_joining(self):
        '''
        Check if a user cannot delete the joining of another user.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/joinings/',
            {
                'event': 1,
                'joining_status': '2'
            },
        )
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.delete('/joinings/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.')
