###CONFTEST

import pytest

from datetime import date, datetime
from typing import List

from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repository import RepositoryException
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist, \
    make_review
from utils import get_project_root

# add_podcast
def test_repository_can_add_a_podcast(in_memory_repo):
    podcast = Podcast(6, Author(6, "test"), "test title", "test image",
                 "test description","www.test.com", None, "test language")
    in_memory_repo.add_podcast(podcast)

    assert in_memory_repo.get_podcasts()[5] is podcast

# get_number_of_podcasts
def test_repository_can_retrieve_podcast_count(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_podcasts()
    print(number_of_podcasts)
    assert number_of_podcasts == 5

# get_episodes
def test_repository_can_retrieve_episodes(in_memory_repo):
    podcast = in_memory_repo.get_podcasts()[0]
    episodes = in_memory_repo.get_episodes(podcast)
    assert episodes[2].title == "#05: Comixology, Runaways, and Star Trek"

# get_number_of_episodes
def test_repository_can_retrieve_episode_count(in_memory_repo):
    podcast = in_memory_repo.get_podcasts()[0]
    assert in_memory_repo.get_number_of_episodes(podcast) == 3


# Add testing
def test_repository_can_add_a_user(in_memory_repo):
    user = User(3,'dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user

def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User(2, 'fmercury', '8734gfe2058v')
    in_memory_repo.add_user(user)

    retrieved_user = in_memory_repo.get_user('fmercury')
    assert retrieved_user == user

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

def test_repository_can_add_a_review(in_memory_repo):
    user = User(1, 'thorke', 'password')
    in_memory_repo.add_user(user)

    podcast = Podcast(2, 'Sample Podcast', '2024-10-01', 'Description')
    in_memory_repo.add_podcast(podcast)

    review = make_review("Interesting!", user, podcast, 3)
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()

def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    podcast = in_memory_repo.get_podcast(2)

    with pytest.raises(TypeError):
        review = Review(None, podcast, 2, "Interesting!")
        in_memory_repo.add_review(review)

def test_repository_does_not_add_a_review_without_a_podcast_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    assert isinstance(user, User)

    podcast = in_memory_repo.get_podcast(2)
    review = Review(user, podcast, 2, "Interesting")

    user.add_review(review)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

def test_repository_can_retrieve_reviews(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    podcast = in_memory_repo.get_podcast(2)

    review1 = make_review("Great podcast!",user, podcast, 5,)
    review2 = make_review("Medium",user, podcast, 2,)

    reviews = in_memory_repo.get_reviews()
    assert len(reviews)==2


def test_repository_can_add_to_user_playlist(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    podcast = in_memory_repo.get_podcast(1)
    episode = in_memory_repo.get_episode(1, 1)
    in_memory_repo.add_to_user_playlist(user, episode)
    in_memory_repo.add_to_user_playlist(user, podcast)

    playlist = user.playlist
    assert episode in playlist._episode_list
    assert podcast in playlist._podcast_list

def test_repository_can_remove_from_user_playlist(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    episode = in_memory_repo.get_episode(1, 1)
    in_memory_repo.add_to_user_playlist(user, episode)

    in_memory_repo.remove_from_user_playlist(user, episode)

    playlist = user.playlist
    assert episode not in playlist._episode_list

def test_repository_can_get_user_playlist(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    episode = in_memory_repo.get_episode(1, 1)
    in_memory_repo.add_to_user_playlist(user, episode)

    playlist = in_memory_repo.get_user_playlist(user)
    assert len(playlist._episode_list) == 1
    assert len(playlist._podcast_list) == 0

def test_repository_can_get_user_podcast_playlist(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    podcast = in_memory_repo.get_podcast(1)
    in_memory_repo.add_to_user_playlist(user, podcast)

    podcast_playlist = in_memory_repo.get_user_podcast_playlist(user)
    assert len(podcast_playlist) == 1

def test_repository_can_get_user_episode_playlist(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    episode = in_memory_repo.get_episode(1, 1)
    in_memory_repo.add_to_user_playlist(user, episode)

    episode_playlist = in_memory_repo.get_user_episode_playlist(user)
    assert len(episode_playlist) == 1

def test_repository_can_get_playlist_total(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        in_memory_repo.add_user(user)

    episode = in_memory_repo.get_episode(1, 1)
    podcast = in_memory_repo.get_podcast(1)

    in_memory_repo.add_to_user_playlist(user, episode)
    in_memory_repo.add_to_user_playlist(user, podcast)

    playlist = in_memory_repo.get_user_playlist(user)
    playlist_total = in_memory_repo.get_playlist_total(playlist)

    assert playlist_total == 2