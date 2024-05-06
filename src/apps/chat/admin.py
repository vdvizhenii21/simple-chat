from django.contrib import admin
from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created", "updated")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "sender", "thread", "created", "is_read")
    list_filter = ("thread", "is_read")
    search_fields = ("sender__username", "thread__participants__username")
