import redis
from django.conf import settings

redis_cli = redis.StrictRedis.from_url(settings.REDIS_URL)
