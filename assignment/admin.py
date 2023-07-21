from django.contrib import admin
from .models import Group, Task


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'name', 'created_date', 'group_uuid')
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['id']


admin.site.register(Task)
