from django.test import TestCase, Client, AsyncClient
from django.urls import reverse

class TestBarViewSet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_collection_wrong_method(self):
        endpoint = reverse('custom_collection')
        response = self.client.get(endpoint)
        # Assuming the endpoint is not allowed for GET requests
        self.assertEqual(response.status_code, 405)

    def test_detail_post_wrong_method(self):
        endpoint = reverse('custom_detail', args=[1])
        response = self.client.post(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_detail_patch_not_found(self):
        endpoint = reverse('custom_detail', args=[1])
        response = self.client.patch(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_detail_patch_found_200(self):
        endpoint = reverse('custom_detail', args=[2])
        response = self.client.patch(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_disabled_endpoint(self):
        endpoint = reverse('custom_some_endpoint')
        response = self.client.get(endpoint)
        # The endpoint exists, but it has the @disable_endpoint decorator on it
        self.assertEqual(response.status_code, 405)

    async def test_async_endpoint(self):
        client = AsyncClient()
        endpoint = reverse('custom_dog')
        response = await client.get(endpoint)
        self.assertEqual(response.status_code, 200)

    async def test_disabled_async_endpoint(self):
        client = AsyncClient()
        endpoint = reverse('custom_cat')
        response = await client.get(endpoint)
        self.assertEqual(response.status_code, 405)

    def test_custom_detail_method(self):
        endpoint = reverse('custom_detail_put', args=[1])
        response = self.client.put(endpoint, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], 7)

    def test_invalid_method_on_custom_detail(self):
        endpoint = reverse('custom_detail_put', args=[1])
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 405)