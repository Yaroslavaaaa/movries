from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *



urlpatterns = [
    path('', MainPage.as_view(), name="index"),
    path('katalog/', Katalog.as_view(), name="katalog"),
    path('movie/<slug:movie_slug>/', MovieInfo.as_view(), name="movie_info"),
    # path('movies/', movie_list, name='movie_list'),
    path('category/<slug:genre_slug>/', MovieCategory.as_view(), name='genre'),
    path('login/', Login.as_view(), name="login_user_page"),
    path('user/<str:user_username>/', UserProfile.as_view(), name="profile"),
    path('movie/<int:pk>/toggle_like/', toggle_like, name='toggle_like'),
    path('movie/<int:pk>/unlike/', unlike, name='unlike'),
    path('profile/liked/', LikedMovies.as_view(), name='liked_movies'),
    path('user/<str:user_username>/editprofile', EditUserProfile.as_view(), name="edit_profile"),
    path('logout/', logout_user, name='logout_user_page'),
    path('register/', Register.as_view(), name="register"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='create_comment'),
    path('<int:pk>/<int:com_pk>/comment_ans/', AnsCommentCreateView.as_view(), name='create_ans_comment'),
]

