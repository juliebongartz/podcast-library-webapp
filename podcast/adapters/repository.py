import abc
from typing import List

from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Author, Category, Episode
repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'Repository exception: {message}')

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, cat: Category):
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_episode(self, episode: Episode):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_podcast(self, podcast: Podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id) -> Podcast:
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self) -> List[Podcast]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes(self, podcast: Podcast) -> List[Episode]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self, podcast: Podcast) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review._poster is None or review not in review._poster._reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review._podcast is None or review not in review._podcast._reviews:
            raise RepositoryException('Review not correctly attached to a Podcast')

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_user_playlist(self, user: User, item: Podcast | Episode):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_user_playlist(self, user: User, item: Podcast | Episode):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_playlist(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_podcast_playlist(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_episode_playlist(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_total(self, playlist: Playlist):
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcasts(self, search_term: str, search_filter: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_count(self):
        raise NotImplementedError