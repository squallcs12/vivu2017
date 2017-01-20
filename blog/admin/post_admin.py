from django.contrib import admin
from django.utils.translation import ugettext as _
from webpush import send_group_notification


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }

    def save_model(self, request, obj, form, change):
        is_new = not obj.pk
        super(PostAdmin, self).save_model(request, obj, form, change)
        if is_new:
            payload = {
                'head': _('New blog post'),
                'options': {
                    'body': obj.title,
                    'data': {
                        'url': obj.get_absolute_url(),
                    }
                },
            }
            send_group_notification(group_name='blog_post', payload=payload, ttl=1000)
