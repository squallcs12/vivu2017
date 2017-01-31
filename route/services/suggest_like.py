import requests
from django.conf import settings
from django.contrib.sites.models import Site

from root.redis import redis_cli
from route.models import Suggest


class SuggestLike:
    KEY = 'SUGGEST_LIKE'

    @classmethod
    def add_id(cls, suggest_id):
        redis_cli.sadd(cls.KEY, suggest_id)

    @classmethod
    def fetch_like(cls):
        ids = redis_cli.srandmember(cls.KEY, 100)

        if not ids:
            return

        redis_cli.srem(cls.KEY, *ids)

        site = Site.objects.get(pk=settings.SITE_ID)
        root_url = 'https://{}'.format(site.domain)

        for suggest_id in ids:
            cls._update_like_count(root_url, int(suggest_id))

    @classmethod
    def _update_like_count(cls, root_url, suggest_id):
        response = requests.get('https://graph.facebook.com/{}/'.format(settings.FACEBOOK_GRAPH_VERSION), params={
            'access_token': settings.FACEBOOK_ACCESS_TOKEN,
            'id': '{}{}'.format(root_url, Suggest(id=suggest_id).get_absolute_url()),
        })

        data = response.json()
        if 'share' in data:
            share_count = data['share'].get('share_count', 0)
            Suggest.objects.filter(id=suggest_id)[0:1].update(like_count=share_count)
