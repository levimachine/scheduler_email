from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from scheduler_email import settings
from users.forms import RegisterForm, UserInputSecretKeyForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:user_login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.secret_key = get_random_secret_key()[:12]
            send_mail(
                subject='Код подтверждения от сайта рассылок',
                message=f'Ваш код подтверждения - {user.secret_key}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            messages.success(request=self.request,
                             message=f'На почту {user.email} отправлено сообщение с секретным ключом.')
        return super().form_valid(form)


class UserInputSecretKey(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserInputSecretKeyForm
    template_name = 'users/user_verify.html'
    success_url = reverse_lazy('mailing_list:home')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_verify = True
            user.save()
            messages.success(request=self.request, message='Верификация успешно пройдена!')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User

    def test_func(self):
        return self.request.user.has_perm('users.deactivate_user')

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False)


class UserDeactivateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('users.deactivate_user')

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        return redirect('users:user_list')
