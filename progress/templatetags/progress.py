from django import template
from django.db.models.aggregates import Sum

from progress.models import Progress

register = template.Library()


def get_default_percentage(progress):
    milestones_count = progress.milestones.all().count()
    custom_percentages = progress.milestones.filter(percentage__gt=0).aggregate(Sum('percentage'))
    custom_percentages_sum = custom_percentages['percentage__sum'] or 0
    return (100 - custom_percentages_sum) / milestones_count


@register.inclusion_tag('progress/progress.html')
def progress(code_name):
    progress = Progress.objects.filter(code_name=code_name).first()
    if not progress:
        return

    default_percentage = get_default_percentage(progress)
    finished_milestones = progress.milestones.finished()
    started_milestones = progress.milestones.started()
    unstarted_milestones = progress.milestones.unstarted()

    finished_percentage = int(sum(x.percentage or default_percentage for x in finished_milestones))
    started_percentage = int(sum(x.percentage or default_percentage for x in started_milestones))
    unstarted_percentage = 100 - finished_percentage - started_percentage

    return {
        'progress': progress,

        'finished_milestones': finished_milestones,
        'started_milestones': started_milestones,
        'unstarted_milestones': unstarted_milestones,

        'finished_percentage': finished_percentage,
        'started_percentage': started_percentage,
        'unstarted_percentage': unstarted_percentage,
    }
