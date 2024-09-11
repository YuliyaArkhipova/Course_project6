from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту",
    )
    full_name = models.CharField(
        max_length=100, verbose_name="Ф.И.О", help_text="Укажите Ф.И.О."
    )
    comment = models.TextField(
        verbose_name="Комментрарий", help_text="Напишите комментарий", **NULLABLE
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "Клиент сервиса"
        verbose_name_plural = "Клиенты сервиса"
        ordering = ("full_name",)

    def __str__(self):
        return self.full_name


class Message(models.Model):

    title = models.CharField(
        max_length=255, verbose_name="Тема письма", help_text="Укажите тему письма"
    )
    message = models.TextField(
        verbose_name="Сообщение", help_text="Введите текст сообщения"
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):

    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    frequency = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    mailing_status = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    status = models.CharField(
        max_length=150,
        choices=mailing_status,
        default=CREATED,
        verbose_name="Статус рассылки",
    )
    periodicity = models.CharField(
        max_length=150,
        choices=frequency,
        default=DAILY,
        verbose_name="Периодичность рассылки",
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала", **NULLABLE, help_text="Укажите дату начала рассылки"
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания",
        **NULLABLE,
        help_text="Укажите дату окончания рассылки",
    )
    next_send_time = models.DateTimeField(
        verbose_name="Время следующей отправки", **NULLABLE
    )
    clients = models.ManyToManyField(
        Client,
        related_name="mailing",
        verbose_name="Выберите клиентов, которым будет отправлена рассылка",
    )
    message = models.ForeignKey(
        Message,
        verbose_name="Cообщение",
        help_text="Укажите текст сообщения",
        on_delete=models.CASCADE,
        **NULLABLE,
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, **NULLABLE
    )

    def __str__(self):
        return f"{self.name}, статус: {self.status}"

    def save(self, *args, **kwargs):
        if not self.next_send_time:
            self.next_send_time = self.start_date
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("name",)
        permissions = [
            ("deactivate_mailing", "Can deactivate mailing"),
            ("view_all_mailings", "Can view all mailings"),
        ]


class Log(models.Model):

    SUCCESS = "Успешно"
    FAIL = "Неуспешно"

    attempt_status = [
        (SUCCESS, "Успешно"),
        (FAIL, "Неуспешно"),
    ]

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.CharField(
        max_length=50, choices=attempt_status, verbose_name="Cтатус рассылки"
    )
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ почтового сервера", **NULLABLE
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )

    def __str__(self):
        return f"{self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
