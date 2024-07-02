from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileTests(APITestCase):

    def setUp(self):
        # Create a user
        User.objects.create_user(
            username='Claudia',
            password='testpassword'
        )
        User.objects.create_user(
            username='Heliot',
            password='testpassword'
        )

    def test_profile_is_created_automaticaly_when_user_is_created(self):
        # Check that a profile is created when a user is created
        user = User.objects.get(username='Claudia')
        profile = Profile.objects.get(owner=user)
        self.assertEqual(profile.owner, user)

    def test_profile_list_is_public_for_authenticated_users(self):
        # Check that the profile list is public for authenticated users
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailTests(APITestCase):

    def setUp(self):
        # Create a user
        User.objects.create_user(
            username='Claudia',
            password='testpassword'
        )
        User.objects.create_user(
            username='Heliot',
            password='testpassword'
        )

    def test_owner_can_see_profile_detail(self):
        # Check that the owner can see the profile detail
        user = User.objects.get(username='Claudia')
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.get(f'/profiles/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_edit_profile(self):
        # Check that the owner can edit the profile
        user = User.objects.get(username='Claudia')
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.put(
            f'/profiles/{user.id}/',
            {
                'name': 'Claudia',
                'feeling': 'happy',
                'would_like_to': 'learn how to code'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_cannot_delete_profile(self):
        # Check that the owner cannot delete the profile
        user = User.objects.get(username='Claudia')
        self.client.login(username='Claudia', password='testpassword')
        response = self.client.delete(f'/profiles/{user.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_other_authenticated_users_cann_see_profile_detail(self):
        # Check that other authenticated users can see the profile detail
        user = User.objects.get(username='Claudia')
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.get(f'/profiles/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_authenticated_users_cannot_edit_profile(self):
        # Check that other authenticated users cannot edit the profile
        user = User.objects.get(username='Claudia')
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.put(
            f'/profiles/{user.id}/',
            {
                'name': 'Claudia',
                'feeling': 'happy',
                'would_like_to': 'learn how to code'
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_authenticated_users_cannot_delete_profile(self):
        # Check that other authenticated users cannot delete the profile
        user = User.objects.get(username='Claudia')
        self.client.login(username='Heliot', password='testpassword')
        response = self.client.delete(f'/profiles/{user.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_users_cannot_edit_profile(self):
        # Check that unauthenticated users cannot edit the profile
        user = User.objects.get(username='Claudia')
        response = self.client.put(
            f'/profiles/{user.id}/',
            {
                'name': 'Claudia',
                'feeling': 'happy',
                'would_like_to': 'learn how to code'
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_users_cannot_delete_profile(self):
        # Check that unauthenticated users cannot delete the profile
        user = User.objects.get(username='Claudia')
        response = self.client.delete(f'/profiles/{user.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
