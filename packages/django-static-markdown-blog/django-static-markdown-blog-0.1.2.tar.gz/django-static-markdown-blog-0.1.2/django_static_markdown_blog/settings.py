from .core.cache import CacheFactory
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os


def _get_blog_folder_settings():
    value = getattr(settings, 'BLOG_FOLDER', None)

    if not value:
        raise ImproperlyConfigured("BLOG_FOLDER settings has to be defined.")

    if not os.path.isdir(value):
        raise ImproperlyConfigured("BLOG_FOLDER settings has to be a directory.")

    return value


BLOG_FOLDER = _get_blog_folder_settings()


def _get_blog_index_file_settings():
    value = getattr(settings, 'BLOG_INDEX_FILE', 'main.md')

    if not value:
        raise ImproperlyConfigured("BLOG_INDEX_FILE has to be defined.")

    if not isinstance(value, str):
        raise ImproperlyConfigured('BLOG_INDEX_FILE has to be a string.')

    return value


BLOG_INDEX_FILE = _get_blog_index_file_settings()


def _get_blog_cache():
    value = getattr(settings, 'BLOG_CACHE', None)

    factory = CacheFactory()
    if value and value not in factory:
        raise ImproperlyConfigured("BLOG_CACHE must be one of them: {}".format([]))

    return value


BLOG_CACHE = _get_blog_cache()


def _get_blog_cache_options():
    if not BLOG_CACHE:
        return dict()

    value = getattr(settings, 'BLOG_CACHE_OPTIONS', {})

    if not isinstance(value, dict):
        raise ImproperlyConfigured("BLOG_CACHE_OPTIONS must be a dictionary.")

    cache_type = getattr(CacheFactory(), BLOG_CACHE)
    if not cache_type:
        raise ImproperlyConfigured("BLOG_CACHE looks improperly configured.")

    if not cache_type.check_options(value):
        raise ImproperlyConfigured("BLOG_CACHE_OPTIONS is not validated by the cache system.")

    return value


BLOG_CACHE_OPTIONS = _get_blog_cache_options()
