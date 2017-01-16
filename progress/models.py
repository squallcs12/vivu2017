from django.db import models
from django.utils.encoding import force_text


class Progress(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey('progress.Milestone', null=True, related_name='belong', blank=True)

    def __str__(self):
        return force_text(self.name)

    class Meta:
        verbose_name_plural = 'Progresses'


class Milestone(models.Model):
    progress = models.ForeignKey('progress.Progress', related_name='milestones')
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    percentage = models.IntegerField(default=0, help_text='0 mean auto calculate')

    def __str__(self):
        return force_text(self.name)

