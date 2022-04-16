from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Movie

class MoviesView(ListView):
    '''Вывод списка фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = 'movies/movies.html'


class MovieDetailView(DetailView):
    '''Вывод одного фильма'''
    model = Movie
    slug_field = 'url'
