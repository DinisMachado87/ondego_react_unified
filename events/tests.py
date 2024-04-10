import os
from django.contrib.auth.models import User
from .models import Event
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class EventTests(APITestCase):

    def setUp(self):
        # Create a user
        User.objects.create_user(
            username='Claudia',
            password='testpassword'
        )

    def test_list_events(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        Event.objects.create(
            owner=claudia,
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
        response = self.client.get('/events/')
        # Check that the event is in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_event(self):
        # Create an image file
        image = Image.new('RGB', (100, 100))
        image.save('test.jpg')
        # Open the image file
        image_file = open('test.jpg', 'rb')
        # Create a Django file object
        image_django = SimpleUploadedFile(image_file.name, image_file.read())
        # Create a user and authenticate
        claudia = User.objects.get(username='Claudia')
        self.client.login(username='Claudia', password='testpassword')
        # Create an event
        response = self.client.post(
            '/events/',
            {
                'what_title': 'Birthday Party',
                'what_content': 'Come celebrate with me!',
                'where_place': '123 Main St',
                'where_address': '123 Main St',
                'when_start': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 12, 0)
                ),
                'when_end': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 14, 0)
                ),
                'intention': 'Cyborg extravaganza!',
                'event_image': image_django  # Use the Django file object here
            }
        )
        # Check that the event was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the event is in the database
        self.assertEqual(Event.objects.count(), 1)
        # Check that the event has the correct title
        self.assertEqual(Event.objects.get().what_title, 'Birthday Party')

        # Close and delete the image file
        image_file.close()
        os.remove('test.jpg')

    def test_unauthenticated_user_cannot_create_event(self):
        # Create an event
        response = self.client.post(
            '/events/',
            {
                'what_title': 'Birthday Party',
                'what_content': 'Come celebrate with me!',
                'where_place': '123 Main St',
                'where_address': '123 Main St',
                'when_start': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 12, 0)
                ),
                'when_end': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 14, 0)
                ),
                'intention': 'Cyborg extravaganza!',
            }
        )
        # Check that the event was not created
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventDetailTests(APITestCase):
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

    def test_logged_in_user_can_retrieve_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Authenticate the user
        self.client.login(username='Claudia', password='testpassword')
        # Retrieve the event
        response = self.client.get(f'/events/{event.id}/')
        # Check that the event is in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_retrieve_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Retrieve the event
        response = self.client.get(f'/events/{event.id}/')
        # Check that the event is in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_update_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Authenticate the user
        self.client.login(username='Claudia', password='testpassword')
        # Update the event
        response = self.client.put(
            f'/events/{event.id}/',
            {
                'what_title': 'Birthday Party',
                'what_content': 'Come celebrate with me!',
                'where_place': '123 Main St',
                'where_address': '123 Main St',
                'when_start': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 12, 0)
                ),
                'when_end': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 14, 0)
                ),
                'intention': 'Cyborg extravaganza!',
            }
        )
        # Check that the event was updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the event has the correct title
        self.assertEqual(Event.objects.get().what_title, 'Birthday Party')

    def test_logged_in_user_cannot_update_other_users_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        heliot = User.objects.get(username='Heliot')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Authenticate the user
        self.client.login(username='Heliot', password='testpassword')
        # Update the event
        response = self.client.put(
            f'/events/{event.id}/',
            {
                'what_title': 'Birthday Party',
                'what_content': 'Come celebrate with me!',
                'where_place': '123 Main St',
                'where_address': '123 Main St',
                'when_start': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 12, 0)
                ),
                'when_end': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 14, 0)
                ),
                'intention': 'Cyborg extravaganza!',
            }
        )
        # Check that the event was not updated
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_update_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Update the event
        response = self.client.put(
            f'/events/{event.id}/',
            {
                'what_title': 'Birthday Party',
                'what_content': 'Come celebrate with me!',
                'where_place': '123 Main St',
                'where_address': '123 Main St',
                'when_start': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 12, 0)
                ),
                'when_end': timezone.make_aware(
                    timezone.datetime(2021, 8, 1, 14, 0)
                ),
                'intention': 'Cyborg extravaganza!',
            }
        )
        # Check that the event was not updated
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Authenticate the user
        self.client.login(username='Claudia', password='testpassword')
        # Delete the event
        response = self.client.delete(f'/events/{event.id}/')
        # Check that the event was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the event is not in the database
        self.assertEqual(Event.objects.count(), 0)

    def test_logged_in_user_cannot_delete_other_users_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        heliot = User.objects.get(username='Heliot')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Authenticate the user
        self.client.login(username='Heliot', password='testpassword')
        # Delete the event
        response = self.client.delete(f'/events/{event.id}/')
        # Check that the event was not deleted
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check that the event is in the database
        self.assertEqual(Event.objects.count(), 1)

    def test_unauthenticated_user_cannot_delete_event(self):
        # Create an event
        claudia = User.objects.get(username='Claudia')
        event = Event.objects.create(
            owner=claudia,
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
        )
        # Delete the event
        response = self.client.delete(f'/events/{event.id}/')
        # Check that the event was not deleted
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check that the event is in the database
        self.assertEqual(Event.objects.count(), 1)
