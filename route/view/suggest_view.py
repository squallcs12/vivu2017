from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from route.serializers.suggest_serializer import SuggestSerializer


class SuggestView(TemplateView):
    template_name = 'route/suggest.html'

    @method_decorator(api_view(['POST']))
    def post(self, request):
        serializer = SuggestSerializer(data=request.data)

        serializer.is_valid(True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
