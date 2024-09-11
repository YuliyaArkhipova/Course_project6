from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    slug = models.CharField(
        max_length=60, verbose_name="slug", help_text="Введите slug", **NULLABLE
    )
    content = models.TextField(
        verbose_name="Текст", help_text="Введите текст", **NULLABLE
    )
    image = models.ImageField(
        upload_to="blogs/",
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        **NULLABLE
    )
    created_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(
        verbose_name="Публикация", help_text="Укажите статус публикации", default=True
    )
    views_count = models.PositiveIntegerField(
        verbose_name="Просмотры", help_text="Количество просмотров", default=0
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title
