from django.conf import settings
from django.core.cache import cache

from blog.models import Post


def get_cache_version_for_post(post_pk):
    if settings.CACHE_ENABLED:
        key = f'post_list{post_pk}'
        post_list = cache.get(key)
        if post_list is None:
            post_list = Post.objects.filter(post__pk=post_pk)
            cache.set(key, post_list)
    else:
        post_list = Post.objects.filter(post__pk=post_pk)
    return post_list