from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'city', 'caste', 'is_staff')
    list_filter = ('is_staff', 'city', 'caste')
    search_fields = ('phone', 'name', 'city')
    ordering = ('-date_joined',)
