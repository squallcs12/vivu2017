from rest_framework import serializers

from route.models import Suggest


class SuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggest
        fields = ('id', 'name', 'address', 'lat', 'lng', 'place_id', 'province', 'description')
