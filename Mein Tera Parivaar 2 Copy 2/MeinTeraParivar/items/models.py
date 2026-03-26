from django.db import models
from django.conf import settings

class ApprovedItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            approval_status='approved',
            is_active=True,
            available_quantity__gt=0
        )
        
    

class Item(models.Model):
    CATEGORY_CHOICES = (
        ('clothes', 'Clothes'),
        ('education', 'Education'),
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('others', 'Others'),
    )

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    )

    APPROVAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    BOARD_TYPE_CHOICES = (
        ('MPBOARD', 'MP Board'),
        ('STATEBOARD', 'State Board'),
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('OTHER', 'Other'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items'
    )

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    description = models.TextField(blank=True)

    # Education-specific fields
    board_type = models.CharField(
        max_length=50,
        choices=BOARD_TYPE_CHOICES,
        blank=True,
        null=True
    )
    dice_code = models.CharField(max_length=20, blank=True, null=True)

    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to='item_images/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='item_videos/',
        blank=True,
        null=True
    )
    
    objects = models.Manager()        # default (admin & internal)
    approved = ApprovedItemManager()  # public

    def save(self, *args, **kwargs):
        # Auto-approve education items
        if self.category == 'education':
            self.approval_status = 'approved'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
