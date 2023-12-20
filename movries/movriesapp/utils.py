from django.db.models import Count
from django.core.cache import cache

from .models import *



class DataMixin:
    # paginate_by = 8
    def get_user_context(self, **kwargs):
        context = kwargs



        if 'genre_selected' not in context:
            context['genre_selected'] = 0

        return context