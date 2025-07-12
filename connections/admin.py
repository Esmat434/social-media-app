from django.contrib import admin

from .models import Connection
# Register your models here.

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','created_at']