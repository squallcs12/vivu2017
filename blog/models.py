from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.encoding import force_text


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return force_text(self.title)

    def get_absolute_url(self):
        return reverse('blog:post', args=(self.slug,))
