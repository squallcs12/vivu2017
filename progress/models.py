from django.db import models
from django.db.models.aggregates import Sum
from django.utils.encoding import force_text


MILESTONE_STATE_UNSTARTED = 0
MILESTONE_STATE_STARTED = 1
MILESTONE_STATE_FINISHED = 2
MILESTONE_STATES = (
    (MILESTONE_STATE_UNSTARTED, 'Unstarted'),
    (MILESTONE_STATE_STARTED, 'Started'),
    (MILESTONE_STATE_FINISHED, 'Finished'),
)


class Progress(models.Model):
    name = models.CharField(max_length=255)
    code_name = models.SlugField(default='', unique=True)
    state = models.ForeignKey('progress.Milestone', null=True, related_name='belong', blank=True)

    def __str__(self):
        return force_text(self.name)

    class Meta:
        verbose_name_plural = 'Progresses'


class MilestoneManager(models.Manager):
    def finished(self):
        return self.get_queryset().filter(state=MILESTONE_STATE_FINISHED)

    def started(self):
        return self.get_queryset().filter(state=MILESTONE_STATE_STARTED)

    def unstarted(self):
        return self.get_queryset().filter(state=MILESTONE_STATE_UNSTARTED)


class Milestone(models.Model):
    progress = models.ForeignKey('progress.Progress', related_name='milestones')
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0, help_text='0 mean auto calculate')
    state = models.IntegerField(choices=MILESTONE_STATES, default=MILESTONE_STATE_UNSTARTED)

    objects = MilestoneManager()

    def __str__(self):
        return force_text(self.name)

