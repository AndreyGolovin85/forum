from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from forum.settings import USER_MIN_AGE


def birth_date_validator(value):
    age_diff = relativedelta(date.today(), value).years
    if age_diff < USER_MIN_AGE:
        raise ValidationError(f"Невозможно зарегистрировать пользователя моложе {USER_MIN_AGE} лет!")
    return value


class User(AbstractUser):
    phone = models.PositiveBigIntegerField(verbose_name="Телефон", null=True)
    birthday = models.DateField(verbose_name="Дата рождения", max_length=10, validators=[birth_date_validator], null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name_user(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий: {self.author} {self.text}"


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="images/", null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    comments = models.ManyToManyField(Comments, verbose_name="Комментарии", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"Пост: {self.author} {self.title}"

    def display_comments(self):
        return ", ".join([comments.text for comments in self.comments.all()])
