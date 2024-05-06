from django.contrib.auth.models import User
from friends.models import Friend, FriendRequest
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone


class FriendRequestTests(APITestCase):
    def setUp(self):
        '''
        Create three users.
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

    def test_logged_in_user_can_create_friend_request(self):
        '''
        Check if a logged in user can create a friend request.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/friends_requests/',
            {
                'to_user': self.heliot.id
            },
        )
        print(response.data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['to_user'], self.heliot.id)
        self.assertEqual(response.data['owner'], self.claudia.id)
        
    def test_logged_in_user_can_accept_friend_request(self):
        '''
        Check if a logged in user can accept a friend request,
        if friends are created automatically through signals,
        and if the friend request is deleted.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/friends_requests/',
            {
                'to_user': self.heliot.id
            },
        )
        # Check if the friend request was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['to_user'], self.heliot.id)
        self.assertEqual(response.data['owner'], self.claudia.id)
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.put(
            '/friends_requests/1/',
            {
                'to_user': self.heliot.id,
                'is_approved': True
            }
        )
        # Check if the friend request was accepted        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_approved'], True)
        # Check if the friends were created automatically through signals
        # Checks if two friends instances were created
        self.assertEqual(Friend.objects.count(), 2)
        # Checks if the friend was created correctly
        # Checks if the friend was created correctly
        self.assertTrue(Friend.objects.filter(owner=self.claudia, friend=self.heliot).exists())
        # Checks if the mirror friend was created correctly
        self.assertTrue(Friend.objects.filter(owner=self.heliot, friend=self.claudia).exists())
        # Check if the friend request was deleted
        self.assertEqual(FriendRequest.objects.count(), 0)

    def test_to_user_can_decline_friend_request(self):
        '''
        Check if a logged in user can decline a friend request.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/friends_requests/',
            {
                'to_user': self.heliot.id
            },
        )
        # Check if the friend request was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['to_user'], self.heliot.id)
        self.assertEqual(response.data['owner'], self.claudia.id)
        self.client.login(username='Heliot', password='testpassword')
        # Delete the friend request
        response = self.client.delete('/friends_requests/1/')
        # Check if the friend request was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FriendRequest.objects.count(), 0)
        
        
    def test_owner_can_delete_friend_request(self):
        '''
        Check if the owner can delete a friend request.
        '''
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.post(
            '/friends_requests/',
            {
                'to_user': self.heliot.id
            },
        )
        # Check if the friend request was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['to_user'], self.heliot.id)
        self.assertEqual(response.data['owner'], self.claudia.id)
        # Delete the friend request
        response = self.client.delete('/friends_requests/1/')
        # Check if the friend request was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FriendRequest.objects.count(), 0)
