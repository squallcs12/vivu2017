from django.conf import settings
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from hashids import Hashids


class Suggest(models.Model):
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    place_id = models.CharField(max_length=255, unique=True)
    province = models.CharField(max_length=80)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    hashid = Hashids(settings.SECRET_KEY)

    def __str__(self):
        return self.address

    @property
    def hash_id(self):
        return self.hashid.encode(self.id)

    @classmethod
    def get_by_hash(cls, hash_id):
        pk = cls.hashid.decode(hash_id)
        if not pk:
            raise Http404()
        return get_object_or_404(cls, pk=pk[0])

    def get_absolute_url(self):
        return reverse('route:suggest-detail', args=(self.hash_id,))
