from django.forms import ModelForm

from mailing.models import Client, Message, Mailing


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = [
            "owner",
        ]
