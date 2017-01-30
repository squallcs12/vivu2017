import random
from urllib import parse

from django.conf import settings
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from googleapiclient.discovery import build
from hashids import Hashids


class Suggest(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    place_id = models.CharField(max_length=255, unique=True)
    province = models.CharField(max_length=80)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    like_count = models.IntegerField(default=0)
    is_chosen = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    google_image = models.URLField(blank=True)
    google_images = ArrayField(models.URLField(), default=[])

    HASHID = Hashids(settings.SECRET_KEY)

    def __str__(self):
        return self.address

    @property
    def hash_id(self):
        return self.HASHID.encode(self.id)

    @classmethod
    def get_by_hash(cls, hash_id):
        pk = cls.HASHID.decode(hash_id)
        if not pk:
            raise Http404()
        return get_object_or_404(cls, pk=pk[0])

    def get_absolute_url(self):
        return reverse('route:suggest-detail', args=(self.hash_id,))

    def get_map_img(self):
        markers = 'color:red|{},{}'.format(self.lat, self.lng)
        params = {
            'center': '{},{}'.format(self.lat, self.lng),
            'zoom': 14,
            'size': '270x300',
            'key': settings.GOOGLE_MAP_API_KEY,
            'markers': markers,
        }
        return 'https://maps.googleapis.com/maps/api/staticmap?{}'.format(parse.urlencode(params))

    def _fetch_google_images(self):
        service = build("customsearch", "v1", developerKey=settings.GOOGLE_MAP_API_KEY)
        res = service.cse().list(
            q=self.name,
            cx='015197566657135856408:nwkhvjx2uog',
            searchType='image',
            num=5,
            imgType='photo',
            cr='vietnam'
        ).execute()

        google_images = [x['link'] for x in res['items']]

        index = random.choice(range(5))

        self.google_image = google_images[index]
        self.google_images = google_images
        self.save()

    def get_google_image(self):
        if not self.google_image:
            self._fetch_google_images()

        return self.google_image

    def get_google_images(self):
        if not self.google_images:
            self._fetch_google_images()

        return self.google_images
