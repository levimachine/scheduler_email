from django.contrib import admin

from mailing_list.models import Client, MailingSettings, Message, MailingAttempt


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'mail')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('mailing_status', 'first_sending_date', 'period')
    list_filter = ('mailing_status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title_message',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_status', 'mail_service_response', 'last_attempt_date')
    list_filter = ('attempt_status',)
