from django.db import models
from django.conf import settings
from items.models import Item


class Request(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    requested_quantity = models.PositiveIntegerField()
    approved_quantity = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.item} by {self.receiver}"
