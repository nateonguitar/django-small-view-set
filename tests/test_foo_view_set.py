from django.test import TestCase, Client
from django.urls import reverse

class TestFooViewSet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_list(self):
        endpoint = reverse('foo_collection')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 1)

    def test_create(self):
        endpoint = reverse('foo_collection')
        response = self.client.post(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['value'], 2)

    def test_retrieve(self):
        endpoint = reverse('foo_details', args=[1])
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 3)

    def test_update(self):
        endpoint = reverse('foo_details', args=[1])
        response = self.client.put(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 4)

    def test_delete(self):
        endpoint = reverse('foo_details', args=[1])
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 204)

    def test_custom_collection_method(self):
        endpoint = reverse('foo_custom')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 6)

    def test_custom_detail_method(self):
        endpoint = reverse('foo_custom_detail', args=[1])
        response = self.client.put(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 7)

    def test_invalid_method_on_custom_detail(self):
        endpoint = reverse('foo_custom_detail', args=[1])
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 405)