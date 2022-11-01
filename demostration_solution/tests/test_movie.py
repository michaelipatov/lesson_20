from unittest.mock import MagicMock

import pytest
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1,
                    title='title_1',
                    description='description_1',
                    trailer='trailer_1',
                    year='2001',
                    rating='6',
                    genre_id='1',
                    director_id='1')

    movie_2 = Movie(id=2,
                    title='title_2',
                    description='description_2',
                    trailer='trailer_2',
                    year='2002',
                    rating='7',
                    genre_id='2',
                    director_id='2')

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock(return_value=None)
    movie_dao.update = MagicMock(return_value=movie_1)

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        assert self.movie_service.get_one(1) is not None
        assert self.movie_service.get_one(1).title == "title_1"

    def test_get_all(self):
        assert len(self.movie_service.get_all()) == 2

    def test_create(self):
        movie_data = {'id': 3,
                      'title': 'title_3',
                      'description': 'description_3',
                      'trailer': 'trailer_3',
                      'year': '2003',
                      'rating': '8',
                      'genre_id': '3',
                      'director_id': '3'}

        new_movie = self.movie_service.create(movie_data)
        assert new_movie.id is not None
        assert 3 == new_movie.id

    def test_update(self):
        movie_data = {'id': 2,
                      'title': 'title_2',
                      'description': 'new_description',
                      'trailer': 'trailer_2',
                      'year': '2002',
                      'rating': '7',
                      'genre_id': '2',
                      'director_id': '2'}

        new_movie = self.movie_service.update(movie_data)
        assert new_movie.id is not None
        assert 'new_description' == new_movie.description

    def test_delete(self):
        assert self.movie_service.delete(1) == None
