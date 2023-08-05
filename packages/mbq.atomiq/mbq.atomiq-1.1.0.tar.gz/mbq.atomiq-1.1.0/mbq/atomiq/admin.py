import json

from django.contrib import admin
from django.utils.html import format_html

import arrow

from . import constants, models


def delete_tasks(modeladmin, request, queryset):
    queryset.update(
        state=constants.TaskStates.DELETED,
        deleted_at=arrow.utcnow().datetime,
    )


delete_tasks.short_description = 'Delete tasks'


def retry_tasks(modeladmin, request, queryset):
    queryset.update(
        state=constants.TaskStates.ENQUEUED,
        visible_after=arrow.utcnow().datetime,
    )


retry_tasks.short_description = 'Retry tasks'


class BaseTaskAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(state=constants.TaskStates.FAILED)

    # disabling the delete action on the listview
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # disabling the delete button when clicking into a single task
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, *args, **kwrargs):
        return False

    def admin_error_message(self, task):
        return format_html(
            '<div style="max-width:500px" >{}</div>',
            task.error_message,
        )

    admin_error_message.short_description = 'error message'

    def admin_stacktrace(self, task):
        return format_html('<br/><pre>{}</pre>', task.stacktrace)

    admin_stacktrace.short_description = 'stacktrace'

    list_display = (
        'id',
        'state',
        'created_at',
        'failed_at',
        'number_of_attempts',
        'admin_error_message',
    )

    fields = (
        'id',
        'state',
        'created_at',
        'failed_at',
        'number_of_attempts',
        'error_message',
        'admin_stacktrace',
    )

    readonly_fields = (
        'id',
        'state',
        'created_at',
        'failed_at',
        'number_of_attempts',
        'error_message',
        'admin_stacktrace',
    )

    actions = [delete_tasks, retry_tasks]


def get_name_from_topic_arn(arn):
    return arn.split(':')[-1]


class SNSTopicListFilter(admin.SimpleListFilter):
    title = 'topic'
    parameter_name = 'topic_arn'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).order_by('topic_arn')
        topic_arns = qs.values_list('topic_arn', flat=True).distinct()
        for arn in topic_arns:
            yield (arn, get_name_from_topic_arn(arn))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(topic_arn=self.value())
        return queryset


class SNSTaskAdmin(BaseTaskAdmin):
    model = models.SNSTask

    def admin_topic(self, task):
        return get_name_from_topic_arn(task.topic_arn)

    admin_topic.short_description = 'topic'

    def admin_payload(self, task):
        return format_html('<br/><pre>{}</pre>', json.dumps(task.payload, indent=4))

    admin_payload.short_description = 'payload'

    list_display = BaseTaskAdmin.list_display + ('admin_topic', )
    list_filter = (SNSTopicListFilter, )
    fields = BaseTaskAdmin.fields + ('topic_arn', 'admin_payload')
    readonly_fields = BaseTaskAdmin.readonly_fields + ('admin_payload', )


def get_name_from_queue_url(url):
    return url.split('/')[-1]


class CeleryTaskAdmin(BaseTaskAdmin):
    model = models.CeleryTask

    def admin_task_arguments(self, task):
        return format_html('<br/><pre>{}</pre>', json.dumps(task.task_arguments, indent=4))

    admin_task_arguments.short_description = 'task arguments'

    list_display = BaseTaskAdmin.list_display + ('task_name', )
    list_filter = ('task_name', )
    fields = BaseTaskAdmin.fields + ('task_name', 'admin_task_arguments')
    readonly_fields = BaseTaskAdmin.readonly_fields + ('task_name', 'admin_task_arguments')


admin.site.register(models.SNSTask, SNSTaskAdmin)
admin.site.register(models.CeleryTask, CeleryTaskAdmin)
