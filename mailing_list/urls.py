from django.urls import path

from mailing_list.apps import MailingListConfig
from mailing_list.views import ClientListView, ClientCreateView, MessageCreateView, MailingSettingsCreateView

app_name = MailingListConfig.name
urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('message_create', MessageCreateView.as_view(), name='message_create'),
    path('mailingsettings_create', MailingSettingsCreateView.as_view(), name='mailingsettings_create')

]
