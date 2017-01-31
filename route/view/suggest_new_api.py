from django.contrib import messages
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from route.serializers.suggest_serializer import SuggestSerializer


class SuggestViewApi(APIView):

    throttle_scope = 'route_suggest'

    def initialize_request(self, request, *args, **kwargs):
        self.http_request = request
        return super(SuggestViewApi, self).initialize_request(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        return SuggestSerializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(True)

        suggest = serializer.save()

        messages.success(self.http_request, _('Cám ơn bạn đã gợi ý một địa điểm hay cho chuyến đi này.'))
        if not suggest.is_approved:
            messages.info(self.http_request, _('Địa điểm sau khi được kiểm duyệt sẽ được hiển thị lên danh sách.'))

        return Response({
            'url': suggest.get_absolute_url(),
        }, status=status.HTTP_201_CREATED)
