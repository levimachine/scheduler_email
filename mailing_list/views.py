from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView, UpdateView
from django_apscheduler.models import DjangoJobExecution, DjangoJob

from blog.models import Blog
from mailing_list.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing_list.management.commands.logger import logger
from mailing_list.models import Client, Message, MailingSettings, MailingAttempt
from dj_scheduler import scheduler, send_email_to_clients
from mailing_list.services import get_cached_queryset


class SelfUserPassesTestMixin(UserPassesTestMixin):
    """Чтобы придерживаться принципа DRY"""
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser or self.get_object().owner == self.request.user


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing_list/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_list'] = Blog.objects.order_by('-publish_date')[:3]
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_list:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        print(self.request.user.pk)
        return get_cached_queryset(self.request.user, Client)


class ClientDetailView(LoginRequiredMixin, SelfUserPassesTestMixin, DetailView):
    model = Client


class ClientDeleteView(LoginRequiredMixin, SelfUserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_list:client_list')


class ClientUpdateView(LoginRequiredMixin, SelfUserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing_list:client_detail', kwargs={'pk': self.object.pk})


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_list:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return get_cached_queryset(self.request.user, Message)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff or self.get_object().owner == self.request.user


class MessageDeleteView(LoginRequiredMixin, SelfUserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_list:message_list')


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing_list:mailingsettings_list')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            mailing_settings = form.save()
            logger.info(f'{mailing_settings.first_sending_date}')
            scheduler.add_job(
                send_email_to_clients,
                trigger=IntervalTrigger(days=mailing_settings.period,
                                        start_date=mailing_settings.first_sending_date),
                id=f'send_email_{mailing_settings.id}',
                max_instances=1,
                replace_existing=True,

                kwargs={'message_id': mailing_settings.message.id, 'mailing_id': mailing_settings.id}
            )
            logger.info('джоба добавлена')
            mailing_settings.save()
        return super().form_valid(form)


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_queryset(self):
        return get_cached_queryset(self.request.user, MailingSettings)


class MailingSettingsDeleteView(LoginRequiredMixin, SelfUserPassesTestMixin, DeleteView):
    model = MailingSettings

    def get_success_url(self):
        scheduler.remove_job(f'send_email_{self.object.pk}')
        return reverse_lazy('mailing_list:mailingsettings_list')


class MailingAttemptDetailView(LoginRequiredMixin, SelfUserPassesTestMixin, DetailView):
    model = MailingAttempt
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['job'] = [job for job in DjangoJob.objects.all() if job.id[-1:] == str(self.object.mailing.pk)][0]
        context['job'] = DjangoJob.objects.get(id=f'send_email_{self.object.mailing.id}')
        context['job_execution'] = [job_execution for job_execution in DjangoJobExecution.objects.all() if
                                    job_execution.job_id == context[
                                        'job'].id]
        context['job_execution_count'] = len(context['job_execution'])
        if len(context['job_execution']) > 0:
            context['job_execution'] = context['job_execution'][0]
        return context


class MailingSettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailingSettings

    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff or self.get_object().owner == self.request.user


class MailingPauseView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        mailing = get_object_or_404(MailingSettings, pk=self.kwargs.get('pk'))
        return self.request.user.is_staff or mailing.owner == self.request.user

    def post(self, request, pk):
        mailing = get_object_or_404(MailingSettings, pk=pk)
        if mailing.mailing_status in ['running', 'created']:
            scheduler.pause_job(job_id=f'send_email_{mailing.pk}')
            mailing.mailing_status = 'completed'
        else:
            scheduler.resume_job(job_id=f'send_email_{mailing.pk}')
            mailing.mailing_status = 'running'
        mailing.save()
        return redirect('mailing_list:mailingsettings_detail', pk=pk)


class StatisticView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'mailing_list/statistic.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = len(MailingSettings.objects.all())
        context['mailing_active'] = len(MailingSettings.objects.exclude(mailing_status='completed'))
        context['clients'] = len(Client.objects.all())
        return context
