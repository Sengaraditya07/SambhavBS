from django.contrib import admin
from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'item',
        'receiver',
        'status',
        'requested_quantity',
        'approved_quantity',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'item__name',
        'receiver__email',
        'receiver__phone',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'accepted_at',
        'completed_at',
    )

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'item',
                'receiver',
                'status',
            )
        }),
        ('Quantity', {
            'fields': (
                'requested_quantity',
                'approved_quantity',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'accepted_at',
                'completed_at',
            )
        }),
    )
