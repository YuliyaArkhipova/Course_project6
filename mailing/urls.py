from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDetailView,
    ClientDeleteView,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    HomeView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    LogListView,
    LogDetailView,
)


app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path(
        "mailing/detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"
    ),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("message/", MessageListView.as_view(), name="message_list"),
    path(
        "message/detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"
    ),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("log/", LogListView.as_view(), name="log_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
