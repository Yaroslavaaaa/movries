from django import template

from movriesapp.models import *

# from movriesapp.models import Genres

# from movriesapp.models import *

register = template.Library()


@register.simple_tag()
def get_genres():
    return Genres.objects.all()

# @register.simple_tag()
# def get_caterory():
#     return Category.objects.all()
#
# @register.simple_tag()
# def get_country():
#     return Country.objects.all()


# @register.inclusion_tag('books/list_genres.html')
# def show_genres():
#     genres = Genres.objects.all()
#     return {"genres": genres}