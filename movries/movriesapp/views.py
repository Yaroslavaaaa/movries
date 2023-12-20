from django.contrib.auth import logout, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, resolve
from django.views import View
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

from .forms import *
from .models import *






class MainPage(View):

    def get(self, request, *args, **kwargs):
        context = {'title': 'Главная страница', 'user': self.request.user}
        return render(request, 'movriesapp/index.html', context)


class Katalog(DataMixin, ListView):
    model = Movie
    template_name = "movriesapp/katalog.html"
    context_object_name = 'movies'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if isinstance(user, AnonymousUser):
            context['liked_movie_ids'] = []
        else:
            context['liked_movie_ids'] = UserLike.objects.filter(user=user).values_list('movie__id', flat=True)
        context['user'] = self.request.user
        genres = Genres.objects.annotate(Count('movie'))
        context['genres'] = genres
        g_def = self.get_user_context(title="Каталог фильмов")
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Movie.objects.filter(is_published=True).select_related('genre')


class MovieCategory(ListView):
    model = Movie
    template_name = 'movriesapp/katalog.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жанр - ' + str(context['movies'][0].genre)
        user = self.request.user
        context['liked_movie_ids'] = UserLike.objects.filter(user=user).values_list('movie__id', flat=True)
        context['genre_selected'] = context['movies'][0].genre.pk
        genres = Genres.objects.annotate(Count('movie'))
        context['genres'] = genres
        return context

    def get_queryset(self):
        return Movie.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).select_related('genre')





class SearchResultsView(DataMixin, ListView):
    model = Movie
    template_name = 'movriesapp/katalog.html'
    context_object_name = 'movies'

    def get_queryset(self):
        query = self.request.GET.get('q')
        movies = Movie.objects.filter(
            Q(title__icontains=query)
        )
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genres.objects.annotate(Count('movie'))
        context['genres'] = genres
        g_def = self.get_user_context(title="Поиск: " + self.request.GET.get('q'))
        return dict(list(context.items()) + list(g_def.items()))






class MovieInfo(DataMixin, DetailView):
    model = Movie
    template_name = "movriesapp/movie_info.html"
    slug_url_kwarg = 'movie_slug'
    context_object_name = 'movie'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        comments = Comments.objects.filter(movie=movie.id).prefetch_related('comments_ans', 'comments_ans__user_com_ans')
        context['form'] = CommentForm()
        context['form_ans'] = AnsCommentForm()
        # comments = movie.comments.filter()
        context['cat_selected'] = 0
        context['comments'] = comments
        g_def = self.get_user_context(title=context['movie'])
        return dict(list(context.items()) + list(g_def.items()))







class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'comment_form.html'


    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.movie = movie
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        movie_slug = self.object.movie.slug
        success_url = reverse('movie_info', kwargs={'movie_slug': movie_slug})
        return success_url





class AnsCommentCreateView(LoginRequiredMixin, CreateView):
    model = CommentsAns
    form_class = AnsCommentForm
    template_name = 'comment_form.html'


    def form_valid(self, form):
        form.instance.user_com_ans_id = self.request.user.id
        form.instance.comments_id = self.kwargs['com_pk']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        movie_slug = movie.slug
        success_url = reverse('movie_info', kwargs={'movie_slug': movie_slug})
        return success_url








class Login(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'movriesapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')





class UserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = "movriesapp/profile.html"
    username_url_kwarg = 'user_username'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.kwargs['user_username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title=context['user'])

        return dict(list(context.items()) + list(g_def.items()))



class EditUserProfile(DataMixin, UpdateView):
    model = CustomUser
    template_name = "movriesapp/edit_profile.html"
    fields = ['first_name', 'last_name', 'username', 'age', 'email', 'avatar']

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('profile', kwargs={'user_username': username})

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['username'].widget.attrs.update({'class': 'form-input'})
        form.fields['age'].widget.attrs.update({'class': 'form-input'})
        form.fields['email'].widget.attrs.update({'class': 'form-input'})
        return form

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title="Редактирование профиля")

        return dict(list(context.items()) + list(g_def.items()))






class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'movriesapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(g_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')






class LikedMovies(DataMixin, ListView):
    model = Movie
    template_name = "movriesapp/liked.html"
    context_object_name = 'movies'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['movies'] = Movie.objects.filter(userlike__user=user)
        context['liked_movie_ids'] = UserLike.objects.filter(user=user).values_list('movie__id', flat=True)
        context['user'] = self.request.user
        g_def = self.get_user_context(title="Список любимых")
        genres = Genres.objects.annotate(Count('movie'))
        context['genres'] = genres
        return dict(list(context.items()) + list(g_def.items()))








def toggle_like(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user_like, created = UserLike.objects.get_or_create(user=request.user, movie=movie)

    if created:
        liked = True
    else:
        user_like.delete()
        liked = False

    url = reverse('katalog')

    return  redirect(url)



def unlike(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user_like, created = UserLike.objects.get_or_create(user=request.user, movie=movie)

    if created:
        liked = True
    else:
        user_like.delete()
        liked = False

    url = reverse('liked_movies')

    return redirect(url)




def logout_user(request):
    logout(request)
    return redirect('login_user_page')