from datetime import datetime

import smtplib
from random import sample

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.mail import send_mail

from blog.models import Blog
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Mailing, Log, Message


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"
        context_data["count_mailing"] = len(Mailing.objects.all())
        count_active_mailings = Mailing.objects.filter().count()
        context_data["count_active_mailings"] = count_active_mailings
        unique_clients_count = Client.objects.filter().distinct().count()
        context_data["count_unique_clients"] = unique_clients_count
        all_posts = list(Blog.objects.filter())
        context_data["random_blog_posts"] = sample(all_posts, min(3, len(all_posts)))
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(user=self.request.user)
        return queryset


class ClientDetailView(DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        new_client = form.save()
        if new_client.user is None:
            new_client.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Рассылки"
        return context_data

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Создать рассылку"
        return context_data

    def get_success_url(self):
        return reverse("mailing:mailing_list")

    def form_valid(self, form):
        new_mailing = form.save()
        new_mailing.owner = self.request.user
        new_mailing.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f"log_list_{self.object.pk}"
            log_list = cache.get(key)
            if log_list is None:
                log_list = self.object.log_set.all()
                cache.set(key, log_list)
        else:
            log_list = self.object.log_set.all()
        context_data["logs"] = log_list

        return context_data


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Обновить рассылку"
        return context_data


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    login_url = "users:login"
    redirect_field_name = "redirect_to"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Создание сообщения"
        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = f"Сообщения"
        return context_data

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = f'Редактирование "{self.object.title}"'
        return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Удаление сообщения"
        return context_data


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Детали сообщения"
        return context_data


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = f"Логи"
        return context_data


class LogDetailView(LoginRequiredMixin, DetailView):
    model = Log
