from django.db import models
from datetime import date

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    '''Категория'''
    name = models.CharField('Категория', max_length=50)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    '''Актеры и режиссеры'''
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    ''''Жанры'''
    name = models.CharField('Жанр', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    '''Фильм'''
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=150, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Год выхода', default=1900)
    country = models.CharField('Страна', max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссеры', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    premier = models.DateField('Дата премьеры', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='В $')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='В $')
    fees_in_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='В $')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_movie', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    '''Кадры из фильма'''
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to='movie_shots/')
    id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'


class RatingStar(models.Model):
    '''Звезда рейтинга'''
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    '''Рейтинг'''
    ip = models.CharField('IP адрес', max_length=15)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'