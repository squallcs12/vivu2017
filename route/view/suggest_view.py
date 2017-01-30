from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
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

        suggest = serializer.save()

        messages.success(self.request, _('Cám ơn bạn đã gợi ý một địa điểm hay cho chuyến đi này.'))
        if not suggest.is_approved:
            messages.info(self.request, _('Địa điểm sau khi được kiểm duyệt sẽ được hiển thị lên danh sách.'))

        return Response({
            'url': suggest.get_absolute_url(),
        }, status=status.HTTP_201_CREATED)
