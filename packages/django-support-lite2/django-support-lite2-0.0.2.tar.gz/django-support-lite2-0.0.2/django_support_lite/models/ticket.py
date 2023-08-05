from django.contrib.auth import get_user_model as user_model
from django.db import models

from django_support_lite.enums import Priority, ResponseType, Status


class TicketManager(models.Manager):
    def count_open(self, user=None):
        query = super().get_queryset().filter(status=Status.OPEN)

        if user:
            query = query.filter(user=user)

        return query.count()

    def count_pending(self):
        return super().get_queryset().filter(
            status=Status.OPEN,
            response_type=ResponseType.USER_RESPONSE
        ).count()

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user_model(), related_name='user', on_delete=models.CASCADE)
    user_close = models.ForeignKey(user_model(), related_name='user_close', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    response_type = models.IntegerField(choices=ResponseType.choices())
    status = models.IntegerField(choices=Status.choices())
    priority = models.IntegerField(choices=Priority.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TicketManager()
