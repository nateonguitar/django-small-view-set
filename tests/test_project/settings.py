from small_view_set import SmallViewSetConfig


SECRET_KEY = "test-secret-key"
DEBUG = True
INSTALLED_APPS = []
ROOT_URLCONF = "test_project.urls"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()