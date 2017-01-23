from django.db import models
from django.utils.encoding import force_text


class Attachment(models.Model):
    file = models.FileField()

    def __str__(self):
        return force_text(self.file)
