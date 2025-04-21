from django.test import TestCase, Client
from django.urls import reverse

class TestBarViewSet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_collection_wrong_method(self):
        endpoint = reverse('bar_collection')
        response = self.client.get(endpoint)
        # Assuming the endpoint is not allowed for GET requests
        self.assertEqual(response.status_code, 405)

    def test_detail_post_wrong_method(self):
        endpoint = reverse('bar_detail', args=[1])
        response = self.client.post(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_detail_patch_not_found(self):
        endpoint = reverse('bar_detail', args=[1])
        response = self.client.patch(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_detail_patch_found_200(self):
        endpoint = reverse('bar_detail', args=[2])
        response = self.client.patch(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)