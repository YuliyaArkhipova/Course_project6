from django.contrib import admin

from mailing.models import Client, Mailing, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment", "user")
    list_filter = ("user",)
    search_fields = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "message", "user")
    list_filter = ("user",)
    search_fields = ("title",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "status",
        "periodicity",
        "start_date",
        "end_date",
        "next_send_time",
        "user",
    )
    list_filter = ("name",)
    search_fields = ("status",)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "status", "server_response", "mailing")
    list_filter = ("server_response",)
    search_fields = ("status",)
