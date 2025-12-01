from django.urls import path

from mailing_list.apps import MailingListConfig
from mailing_list.views import ClientCreateView, MessageCreateView, MailingSettingsCreateView, HomeView, ClientListView, \
    ClientDetailView, ClientDeleteView, MessageListView, MessageDetailView, MessageDeleteView, MailingSettingsListView, \
    MailingSettingsDetailView, MailingSettingsDeleteView, ClientUpdateView, MailingAttemptDetailView

app_name = MailingListConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('message_create', MessageCreateView.as_view(), name='message_create'),
    path('mailingsettings_create', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),

    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_detail/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path('client_detail/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),

    path('message_list', MessageListView.as_view(), name='message_list'),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message_detail/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    path('mailingsettings_list', MailingSettingsListView.as_view(), name='mailingsettings_list'),
    path('mailingsettings_detail/<int:pk>', MailingSettingsDetailView.as_view(), name='mailingsettings_detail'),
    path('mailingsettings_detail/<int:pk>/delete', MailingSettingsDeleteView.as_view(), name='mailingsettings_delete'),
    path('mailingsettings_detail/attempt/<str:slug>', MailingAttemptDetailView.as_view(), name='mailingsettings_attempt')
]
