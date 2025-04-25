from django.test import TestCase, Client
from django.urls import reverse

class TestCustomProtectionsViewSet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_options_and_head_collection(self):
        endpoint = reverse('custom_protections_collection')
        response = self.client.options(endpoint)
        self.assertEqual(response.status_code, 200)
        response = self.client.head(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_options_and_head_details(self):
        endpoint = reverse('custom_protections_detail', args=[1])
        response = self.client.options(endpoint)
        self.assertEqual(response.status_code, 200)
        response = self.client.head(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_post_required_logged_in(self):
        endpoint = reverse('custom_protections_collection')
        response = self.client.post(
            endpoint,
            data={},
            content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_post_requires_verified_user(self):
        endpoint = reverse('custom_protections_collection')
        # Unverified user
        response = self.client.post(
            endpoint,
            headers={
                'Authorization': 'Bearer logged_in_but_not_verified'
            },
            data={},
            content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_post_success(self):
        endpoint = reverse('custom_protections_collection')

        # Verified user
        response = self.client.post(
            endpoint,
            headers={
                'Authorization': 'Bearer logged_in_and_verified'
            },
            data={},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)