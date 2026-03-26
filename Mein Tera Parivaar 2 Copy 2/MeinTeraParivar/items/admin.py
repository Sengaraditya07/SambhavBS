from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'condition',
        'owner',
        'total_quantity',
        'available_quantity',
        'approval_status',
        'is_active',
        'created_at',
    )

    list_filter = (
        'approval_status',
        'category',
        'condition',
        'is_active',
    )

    search_fields = (
        'name',
        'owner__phone',
    )

    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'owner',
                'name',
                'category',
                'condition',
                'description',
                'image',
                'video',
            )
        }),
        ('Quantity', {
            'fields': (
                'total_quantity',
                'available_quantity',
                'is_active',
            )
        }),
        ('Moderation', {
            'fields': (
                'approval_status',
                'rejection_reason',
            )
        }),
        ('System Info', {
            'fields': (
                'created_at',
            )
        }),
    )
    readonly_fields = (
        'created_at',
    )