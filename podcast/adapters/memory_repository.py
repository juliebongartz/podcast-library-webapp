import abc
from pathlib import Path
from bisect import insort_left
from typing import List
import os

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Author, Episode, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from utils import get_project_root


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = []
        self.__users = []
        self.__reviews = []
        self.__authors = []
        self.__categories = []
        self.__episodes = []

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

    def add_podcast(self, podcast: Podcast):
        if isinstance(podcast, Podcast):
            insort_left(self.__podcasts, podcast)

    def get_podcast(self, podcast_id) -> Podcast:
        return next((podcast for podcast in self.__podcasts if podcast._id == podcast_id), None)

    def get_podcasts(self) -> List[Podcast]:
        return self.__podcasts

    def get_number_of_podcasts(self):
        return len(self.__podcasts)

    def get_episode(self, podcast_id, episode_id) -> Episode:
        return next((episode for episode in self.get_episodes(self.get_podcast(podcast_id)) if episode.id == episode_id), None)

    def get_episodes(self, podcast: Podcast) -> List[Episode]:
        return podcast.episodes

    def get_number_of_episodes(self, podcast: Podcast) -> int:
        return len(podcast.episodes)

    def add_review(self, review: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)
        review._poster._reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def add_to_user_playlist(self, user: User, item: Podcast | Episode):
        playlist = user.playlist
        playlist.add_item(item)

    def remove_from_user_playlist(self, user: User, item: Podcast | Episode):
        playlist = user.playlist
        if isinstance(item, Episode):
            playlist._episode_list.remove(item)
        elif isinstance(item, Podcast):
            playlist._podcast_list.remove(item)

    def get_user_playlist(self, user: User) -> Playlist:
        return user.playlist

    def get_user_podcast_playlist(self, user: User):
        playlist = user.playlist
        return playlist.podcast_list

    def get_user_episode_playlist(self, user: User):
        playlist = user.playlist
        return playlist.episode_list

    def get_playlist_total(self, playlist: Playlist):
        return len(playlist._podcast_list) + len(playlist._episode_list)

    def search_podcasts(self, search_term: str, search_filter: str):
        results = []

        if search_term != "":
            if search_filter == "Title":
                for podcast in self.__podcasts:
                    if search_term.lower() in podcast.title.lower():
                        results.append(podcast)

            if search_filter == "Category":
                for podcast in self.__podcasts:
                    for category in podcast.categories:
                        if search_term.lower() in category.name.lower():
                            results.append(podcast)

            if search_filter == "Author":
                for podcast in self.__podcasts:
                    if search_term.lower() in podcast.author.name.lower():
                        results.append(podcast)

            if search_filter == "Language":
                for podcast in self.__podcasts:
                    if search_term.lower() in podcast.language.lower():
                        results.append(podcast)

        return results

    def add_author(self, author: Author):
        if isinstance(author, Author) and (author not in self.__authors):
            insort_left(self.__authors, author)

    def add_category(self, category: Category):
        if isinstance(category, Category) and (category not in self.__categories):
            insort_left(self.__categories, category)

    def add_episode(self, episode: Episode):
        if isinstance(episode, Episode) and (episode not in self.__episodes):
            insort_left(self.__episodes, episode)

    def get_user_count(self):
        return len(self.__users)

    def remove_episode(self, episode: Episode):
        self.__episodes.remove(episode)

    def remove_podcast(self, podcast: Podcast):
        self.__podcasts.remove(podcast)


def populate(data_path: Path, repo: AbstractRepository):
    reader = CSVDataReader()

    reader.read_podcasts(data_path) #data path paramter
    reader.read_episodes(data_path) # data path parameter

    if data_path == get_project_root() / "tests" / "data":
        reader.read_users(data_path)  # data path paramter
        reader.read_reviews(data_path)  # data path paramter

        users = reader.dataset_of_users
        for user in users:
            repo.add_user(user)

        reviews = reader.dataset_of_reviews
        for review in reviews:
            repo.add_review(review)
            review._poster.add_review(review)
            review._podcast.add_review(review)

    podcast = reader.dataset_of_podcasts
    for podcast in podcast:
        repo.add_podcast(podcast)

