from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.


# admin.site.register(Movries)

class MoviesAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ('is_published', 'title', 'director', 'genre', 'get_html_photo', 'year', 'slug', 'country', 'release_date')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('get_html_photo', )
    save_on_top = True

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")

    def actors(self, obj):
        return ", ".join([actor.name for actor in obj.actors.all()])

    def genre(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    actors.short_description = "Актеры"

    get_html_photo.short_description = "Миниатюра"


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    list_display_links = ('id', 'genre_name')
    search_fields = ('genre_name',)
    prepopulated_fields = {"slug": ("genre_name",)}




class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'com_text', 'movie', 'user')
    list_display_links = ('id', 'com_text')
    search_fields = ('com_text',)
    # prepopulated_fields = {"slug": ("genre_name",)}

class AnsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ans_com_text', 'user_com_ans', 'comments')
    list_display_links = ('id', 'ans_com_text')
    search_fields = ('ans_com_text',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')
    list_display_links = ('id', 'role_name')
    search_fields = ('role_name',)



class UserLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie')
    list_display_links = ('id', 'user', 'movie')
    search_fields = ('id',)



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    search_fields = ('username',)

    def get_html_avatar(self, object):
        if object.avatar:
            return mark_safe(f"<img src='{object.avatar.url}' width=50>")

    get_html_avatar.short_description = "Миниатюра"


# class EmployeeInline(admin.StackedInline):
#     model = CustomUser
#     can_delete = False
#     verbose_name_plural = 'employee'




admin.site.register(Movie, MoviesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Roles, RoleAdmin)
admin.site.register(UserLike, UserLikeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CommentsAns, AnsCommentAdmin)

admin.site.site_title = 'Админ-панель сайта с обзорами фильмов и сериалов'
admin.site.site_header = 'Админ-панель сайта с обзорами фильмов и сериалов'
