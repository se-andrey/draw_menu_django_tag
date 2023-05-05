from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'parent', 'menu_name')
    list_filter = ('menu_name',)
    search_fields = ('title',)
