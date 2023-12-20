from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from movries import settings


# from .movries import settings


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name="Название")
    director = models.CharField(max_length=255, verbose_name="Режиссер")
    genre = models.ForeignKey("Genres", verbose_name="Жанр", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Описание")
    year = models.IntegerField(verbose_name="Год выпуска")
    image = models.ImageField(upload_to="photos/bookphoto/%Y/%m/%d/", verbose_name="Изображение")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    country = models.ForeignKey("Country", on_delete=models.CASCADE, verbose_name="Страна")
    screenwriter = models.CharField(max_length=255, verbose_name="Сценарист")
    produser = models.CharField(max_length=255, verbose_name="Продюсер")
    duration = models.IntegerField(verbose_name="Длительность, минут")
    release_date = models.DateField()
    actors = models.ManyToManyField("Actor", verbose_name="Актеры")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film', kwargs={'film_slug': self.slug})

    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = 'Фильмы'
        ordering = ['title']




class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country', kwargs={'country_slug': self.slug})


    class Meta:
        verbose_name = 'Страны'
        verbose_name_plural = 'Страны'
        ordering = ['name']



class Actor(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor', kwargs={'actor_slug': self.slug})

    class Meta:
        verbose_name = 'Актеры'
        verbose_name_plural = 'Актеры'
        ordering = ['name']


class Genres(models.Model):
    genre_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


    def __str__(self):
        return self.genre_name


    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'
        ordering = ['id']







class CustomUser(AbstractUser):
    # Добавляем новые поля в модель пользователя
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='photos/avatars/%Y/%m/%d/', default='photos/avatars/no_avatar.jpg')
    role = models.ForeignKey("Roles", on_delete=models.PROTECT, default=1)


    def __str__(self):
        return self.username


    def get_absolute_url(self):
        return reverse('user', kwargs={'user_username': self.username})



class Roles(models.Model):
    role_name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.role_name



    class Meta:
        verbose_name = 'Роли'
        verbose_name_plural = 'Роли'
        ordering = ['role_name']

class Comments(models.Model):
    com_text = models.TextField(db_index=True, verbose_name="Текст комментария")
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="comments", verbose_name="Фильм")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.com_text

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.movie.pk})


    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['create_time', 'com_text']




class CommentsAns(models.Model):
    ans_com_text = models.TextField(db_index=True, verbose_name="Текст комментария")
    user_com_ans = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    comments = models.ForeignKey("Comments", on_delete=models.CASCADE, related_name="comments_ans", verbose_name="Комментарий")

    def __str__(self):
        return self.ans_com_text

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.comments.pk})

    class Meta:
        verbose_name = 'Ответы на комментарии'
        verbose_name_plural = 'Ответы на комментарии'
        ordering = ['create_time', 'ans_com_text']


class UserLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"


    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'
        ordering = ['pk']