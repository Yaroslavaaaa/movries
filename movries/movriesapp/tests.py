from django.test import TestCase
from .models import *
class MovieCase(TestCase):
    def setUp(self):
        Movie.objects.create(
            title="Тестовый фильм",
            director="Тестовый режиссер",
            genre=Genres.objects.create(genre_name="Тестовый жанр"),
            type=Type.objects.create(film_type="Тестовый тип"),
            description="Тестовое описание",
            year=2022,
            image="path/to/test/image.jpg",
            slug="test-movie",
            is_published=True,
            country=Country.objects.create(name="Тестовая страна"),
            screenwriter="Тестовый сценарист",
            produser="Тестовый продюсер",
            duration=120,
            release_date="2022-01-01",
            category=Category.objects.create(name="Тестовая категория"),
        )

    def test_get_movie_by_slug(self):
        movie = Movie.objects.get(slug="test-movie")
        self.assertEqual(movie.title, "Тестовый фильм")
        self.assertEqual(movie.director, "Тестовый режиссер")




class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Тестовая категория", slug="test-category")

    def test_get_category_by_slug(self):
        category = Category.objects.get(slug="test-category")
        self.assertEqual(category.name, "Тестовая категория")


class CountryTestCase(TestCase):
    def setUp(self):
        Country.objects.create(name="Тестовая страна", slug="test-country")

    def test_get_country_by_slug(self):
        country = Country.objects.get(slug="test-country")
        self.assertEqual(country.name, "Тестовая страна")


class ActorTestCase(TestCase):
    def setUp(self):
        Actor.objects.create(name="Тестовый актер", slug="test-actor")

    def test_get_actor_by_slug(self):
        actor = Actor.objects.get(slug="test-actor")
        self.assertEqual(actor.name, "Тестовый актер")


class GenresTestCase(TestCase):
    def setUp(self):
        Genres.objects.create(genre_name='Тестовый жанр', slug='test-name')

    def test_genre(self):
        genre = Genres.objects.get(slug="test-name")
        self.assertEqual(genre.genre_name, 'Тестовый жанр')



class CustomUserTestCase(TestCase):
    def setUp(self):
        role = Roles.objects.create(role_name="Тестовая роль")
        CustomUser.objects.create(username="testuser", role=role, password="12345")

    def test_get_user_by_username(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.username, "testuser")


class CommentsTestCase(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            title="Тестовый фильм",
            director="Тестовый режиссер",
            genre=Genres.objects.create(genre_name="Тестовый жанр"),
            type=Type.objects.create(film_type="Тестовый тип"),
            description="Тестовое описание",
            year=2022,
            image="path/to/test/image.jpg",
            slug="test-movie",
            is_published=True,
            country=Country.objects.create(name="Тестовая страна"),
            screenwriter="Тестовый сценарист",
            produser="Тестовый продюсер",
            duration=120,
            release_date="2022-01-01",
            category=Category.objects.create(name="Тестовая категория"),
        )
        role = Roles.objects.create(role_name="Тестовая роль")
        user = CustomUser.objects.create(username="testuser", role=role, password="12345")
        Comments.objects.create(com_text="Тестовый комментарий", movie=movie, user=user)

    def test_get_comment_by_text(self):
        comment = Comments.objects.get(com_text="Тестовый комментарий")
        self.assertEqual(comment.com_text, "Тестовый комментарий")