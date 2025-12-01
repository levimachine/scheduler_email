from apscheduler.triggers.cron import CronTrigger
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView, UpdateView
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution, DjangoJob

from mailing_list.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing_list.management.commands.logger import logger
from mailing_list.models import Client, Message, MailingSettings, MailingAttempt
from dj_scheduler import scheduler, send_email_to_clients


class HomeView(TemplateView):
    template_name = 'mailing_list/home.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_list:client_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_list:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing_list:client_detail', kwargs={'pk': self.object.pk})


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_list:message_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_list:message_list')


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing_list:mailingsettings_list')

    def form_valid(self, form):
        if form.is_valid():
            mailing_settings = form.save()
            logger.info(f'{mailing_settings.first_sending_date}')
            scheduler.add_job(
                send_email_to_clients,
                trigger=CronTrigger(second=f'*/{mailing_settings.period}',
                                    start_date=mailing_settings.first_sending_date),
                id=f'send_email_{mailing_settings.id}',
                max_instances=1,
                replace_existing=True,

                kwargs={'message_id': mailing_settings.message.id, 'mailing_id': mailing_settings.id}
            )
            logger.info('джоба добавлена')
            mailing_settings.save()
        return super().form_valid(form)


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings


    def get_success_url(self):
        scheduler.remove_job(f'send_email_{self.object.pk}')
        print(self.object.pk)
        return reverse_lazy('mailing_list:mailingsettings_list')


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = [job for job in DjangoJob.objects.all() if job.id[-2:] == str(self.object.mailing.pk)][0]
        context['job_execution'] = [job_execution for job_execution in DjangoJobExecution.objects.all() if job_execution.job_id == context[
                                        'job'].id]
        context['job_execution_count'] = len(context['job_execution'])
        if len(context['job_execution']) > 0:
            context['job_execution'] = context['job_execution'][0]
        return context


class MailingSettingsDetailView(DetailView):
    model = MailingSettings
