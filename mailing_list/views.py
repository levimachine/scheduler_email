from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from mailing_list.models import Client, Message, MailingSettings


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('mail', 'fullname', 'comment')
    success_url = reverse_lazy('mailing_list:client_list')


class MessageCreateView(CreateView):
    model = Message
    fields = ('title_message', 'body_message')
    success_url = reverse_lazy('mailing_list:client_list')


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    fields = ('first_sending_date', 'period', 'mailing_status', 'message', 'client')
    success_url = reverse_lazy('mailing_list:client_list')


    def get_object(self, queryset = None):

        from mailing_list.management.commands.runapscheduler import Command

