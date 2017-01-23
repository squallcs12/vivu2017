from django.contrib import admin
from webpush import models as webpush_models

from common.admin.attachment_admin import AttachmentAdmin
from common.models import Attachment

from . import webpush_admin

admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(webpush_models.Group)
admin.site.register(webpush_models.PushInformation, webpush_admin.PushInformationAdmin)
admin.site.register(webpush_models.SubscriptionInfo, webpush_admin.SubscriptionInfoAdmin)


webpush_models.Group.__str__ = lambda self: self.name
webpush_models.SubscriptionInfo.__str__ = lambda self: self.browser
