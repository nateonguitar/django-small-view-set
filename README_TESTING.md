# Testing with Django Small View Set

This guide demonstrates how to test endpoints created with the Django Small View Set library using the standard Django test framework tools.

## Example Test Cases

Remember to register SmallViewSetConfig in settings:
```python
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(exception_handler=app_exception_handler)
```

Remember to include `content_type="application/json"` in requests for proper handling.

```python
import datetime
from django.test import TestCase, Client, override_settings
from django.utils import timezone
from django.urls import reverse
from api.models import (
    ForumPost,
    User,
)


class Test(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user_normal = User.objects.create(
            username='user_normal',
            email='user_normal@email.com',
            email_verified=True,
            recaptcha_score=0.9,
            recaptcha_score_recorded_at=timezone.now())
        self.user_suspected_bot = User.objects.create(
            username='user_suspected_bot',
            email='user_suspected_bot@email.com',
            email_verified=True,
            recaptcha_score=0.25,
            recaptcha_score_recorded_at=timezone.now())

    def test_get_forum_posts_not_logged_in(self):
        endpoint = reverse('forum_posts_collection')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_create_forum_post_fails_not_logged_in(self):
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_collection')
        response = self.client.post(endpoint, data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_forum_post_fails_suspected_bot(self):
        self.client.force_login(self.user_suspected_bot)
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_collection')
        response = self.client.post(endpoint, data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_create_forum_post_fails_bad_tags(self):
        self.client.force_login(self.user_normal)
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_collection')
        response = self.client.post(
            endpoint,
            { **data, 'title': 'Title <script>this is a script</script>' },
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            endpoint,
            { **data, 'title': 'Title <iframe>this is a script</iframe>' },
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            endpoint,
            { **data, 'text': 'Text <script>this is a script</script>' },
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            endpoint,
            { **data, 'text': 'Text <iframe>this is a script</iframe>' },
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_forum_post_success(self):
        self.client.force_login(self.user_normal)
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_collection')
        response = self.client.post(endpoint, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_update_forum_post_fails_not_logged_in(self):
        forum_post = ForumPost.objects.create(
            user=self.user_normal,
            title='Forum post',
            text='Post body')
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_detail', args=[forum_post.id])
        response = self.client.put(endpoint, data, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_forum_post_fails_suspected_bot(self):
        self.client.force_login(self.user_suspected_bot)
        forum_post = ForumPost.objects.create(
            user=self.user_normal,
            title='Forum post 1',
            text='Post body')
        data = {
            'blog': True,
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_detail', args=[forum_post.id])
        response = self.client.put(endpoint, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_update_forum_post_fails_bad_tags(self):
        self.client.force_login(self.user_normal)
        data = {
            'title': 'Title',
            'text': 'Text',
        }
        forum_post = ForumPost.objects.create(
            user=self.user_normal,
            title='Forum post 1',
            text='Post body')
        endpoint = reverse('forum_posts_detail', args=[forum_post.pk])
        response = self.client.put(
            endpoint,
            { **data, 'title': 'Title <script>this is a script</script>' },
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put(
            endpoint,
            { **data, 'title': 'Title <iframe>this is a script</iframe>' },
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put(
            endpoint,
            { **data, 'text': 'Text <script>this is a script</script>' },
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put(
            endpoint,
            { **data, 'text': 'Text <iframe>this is a script</iframe>' },
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_forum_post_success(self):
        self.client.force_login(self.user_normal)
        forum_post = ForumPost.objects.create(
            user=self.user_normal,
            title='Forum post 1',
            text='Post body')
        data = {
            'title': 'Title',
            'text': 'Text',
        }
        endpoint = reverse('forum_posts_detail', args=[forum_post.id])
        response = self.client.put(endpoint, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @override_settings(LIST_PAGE_SIZES={'FORUM_POSTS': 2})
    def test_get_page_of_posts(self):
        forum_post_1 = ForumPost.objects.create(
            user=self.user_normal,
            title='Stinky Bucket',
            text='Post body',
            latest_update_at=timezone.datetime(2024, 10, 2, 0, 0, 0, tzinfo=datetime.timezone.utc))
        forum_post_2 = ForumPost.objects.create(
            user=self.user_normal,
            title='Cat in the street car',
            text='Post body',
            blog=True,
            latest_update_at=timezone.datetime(2024, 10, 9, 0, 0, 0, tzinfo=datetime.timezone.utc))
        forum_post_3 = ForumPost.objects.create(
            user=self.user_normal,
            title='OMG This site is awesome',
            text='Post body',
            latest_update_at=timezone.datetime(2024, 10, 15, 0, 0, 0, tzinfo=datetime.timezone.utc))

        self.client.force_login(self.user_normal)
        endpoint = reverse('forum_posts_collection')

        # Get page 1, no page param
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 2)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 2)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_3.id, forum_post_2.id])

        # Get page 1, no page param
        response = self.client.get(f'{endpoint}?page=1')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 2)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 2)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_3.id, forum_post_2.id])

        # Get page 2
        response = self.client.get(f'{endpoint}?page=2')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 2)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 1)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_1.id])

        # Get page 1, filter by search
        response = self.client.get(f'{endpoint}?search=this+site')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 1)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 1)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_3.id])

        # Get page 1, filter by blog
        response = self.client.get(f'{endpoint}?blog=true')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 1)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 1)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_2.id])

        # Get page 1, filter by non-blog
        response = self.client.get(f'{endpoint}?blog=false')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['pages'], 1)
        response_posts = response_data['results']
        self.assertEqual(len(response_posts), 2)
        self.assertEqual([x['id'] for x in response_posts], [forum_post_3.id, forum_post_1.id])
```

## Key Points

- Use `content_type="application/json"` in requests to ensure proper handling.
- Leverage Django’s `TestCase` and `Client` for testing endpoints.
- Use `reverse` to do lookups from the endpoint names.
- Register `SmallViewSetConfig` in settings for custom exception and options/head handlers.
