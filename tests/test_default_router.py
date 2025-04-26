from django.test import TestCase, Client
from django.urls import reverse

class TestBasicCrudViewSet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_options_and_head_collection(self):
        endpoint = reverse('basic_crud_collection')
        response = self.client.options(endpoint)
        self.assertEqual(response.status_code, 200)
        response = self.client.head(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_options_and_head_details(self):
        endpoint = reverse('basic_crud_details', args=[1])
        response = self.client.options(endpoint)
        self.assertEqual(response.status_code, 200)
        response = self.client.head(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        endpoint = reverse('basic_crud_collection')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 1)

    def test_create(self):
        endpoint = reverse('basic_crud_collection')
        response = self.client.post(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['value'], 2)

    def test_retrieve(self):
        endpoint = reverse('basic_crud_details', args=[1])
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 3)

    def test_update(self):
        endpoint = reverse('basic_crud_details', args=[1])
        response = self.client.put(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 4)

    def test_delete_fails_wrong_http_method(self):
        endpoint = reverse('basic_crud_details', args=[1])
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 204)