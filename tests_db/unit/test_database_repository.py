from datetime import date, datetime
from typing import List

import pytest

from podcast.domainmodel.model import User, Podcast, Review, make_review, Author, Episode
from podcast.adapters.repository import RepositoryException


def test_repository_can_add_a_user(database_repo):
    user = User(3, 'dave', '123456789')
    database_repo.add_user(user)

    assert database_repo.get_user('dave') == user


def test_repository_can_retrieve_a_user(database_repo):
    user = User(2, 'fmercury', '8734gfe2058v')
    database_repo.add_user(user)

    retrieved_user = database_repo.get_user('fmercury')
    assert retrieved_user == user


def test_repository_does_not_retrieve_a_non_existent_user(database_repo):
    user = database_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_podcast_count(database_repo):
    for podcast in database_repo.get_podcasts():
        database_repo.remove_podcast(podcast)

        # Add exactly 5 podcasts for this test
    for i in range(5):
        podcast = Podcast(i, Author(i, f"Author {i}"), f"Title {i}", "image.png", "description", "www.test.com", None,
                          "English")
        database_repo.add_podcast(podcast)

    number_of_podcasts = database_repo.get_number_of_podcasts()
    assert number_of_podcasts == 5


def test_repository_can_add_a_podcast(database_repo):
    podcast = Podcast(6, Author(6, "test"), "test title", "test image",
                      "test description", "www.test.com", None, "test language")
    database_repo.add_podcast(podcast)

    assert database_repo.get_podcasts()[5] == podcast


def test_repository_can_retrieve_episodes(database_repo):
    podcast = database_repo.get_podcasts()[0]
    episodes = database_repo.get_episodes(podcast)
    assert episodes[2].title == "#05: Comixology, Runaways, and Star Trek"


def test_repository_can_retrieve_episode_count(database_repo):
    podcast = database_repo.get_podcast(3)

    assert database_repo.get_number_of_episodes(podcast) == 2

def test_repository_can_add_a_review(database_repo):
    user = database_repo.get_user('thorke')
    podcast = database_repo.get_podcast(2)

    review = make_review("Interesting!", user, podcast, 3)
    database_repo.add_review(review)
    reviews = database_repo.get_reviews()

    assert reviews[-1]._comment == review._comment


def test_repository_does_not_add_a_review_without_a_user(database_repo):
    podcast = database_repo.get_podcast(2)

    with pytest.raises(TypeError):
        review = Review(None, podcast, 2, "Interesting!")
        database_repo.add_review(review)

def test_repository_does_not_add_a_review_without_a_podcast_properly_attached(database_repo):
    user = database_repo.get_user('thorke')

    with pytest.raises(TypeError):
        podcast = database_repo.get_podcast(2)
        review = Review(user, None,2, "Interesting")

        user.add_review(review)
        database_repo.add_review(review)

def test_repository_can_retrieve_reviews(database_repo):
    #user = User(1, 'thorke', 'password')
    user = User(1, 'thorke', 'password')
    database_repo.add_user(user)
    podcast = database_repo.get_podcast(3)
    #podcast = Podcast(2, 'Test Podcast', 'Description', 'Author')

    review1 = Review(user, podcast, 5, "Great podcast!")
    review2 = Review(user, podcast, 4, "Good content!")

    database_repo.add_review(review1)
    database_repo.add_review(review2)

    reviews = database_repo.get_reviews()
    assert reviews[-1]._comment == review2._comment
    assert reviews[-2]._comment == review1._comment


def test_repository_can_add_to_user_playlist(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    podcast = database_repo.get_podcast(1)
    episode = database_repo.get_episode(1, 1)
    database_repo.add_to_user_playlist(user, episode)
    database_repo.add_to_user_playlist(user, podcast)

    playlist = user.playlist
    assert episode in playlist._episode_list
    assert podcast in playlist._podcast_list


def test_repository_can_remove_from_user_playlist(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    episode = database_repo.get_episode(1, 1)
    database_repo.add_to_user_playlist(user, episode)

    database_repo.remove_from_user_playlist(user, episode)

    playlist = user.playlist
    assert episode not in playlist._episode_list


def test_repository_can_get_user_playlist(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    episode = database_repo.get_episode(1, 1)
    database_repo.add_to_user_playlist(user, episode)

    playlist = database_repo.get_user_playlist(user)
    assert len(playlist._episode_list) == 1
    assert len(playlist._podcast_list) == 0


def test_repository_can_get_user_podcast_playlist(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    podcast = database_repo.get_podcast(1)
    database_repo.add_to_user_playlist(user, podcast)

    podcast_playlist = database_repo.get_user_podcast_playlist(user)
    assert len(podcast_playlist) == 1


def test_repository_can_get_user_episode_playlist(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    episode = database_repo.get_episode(1, 1)
    database_repo.add_to_user_playlist(user, episode)

    episode_playlist = database_repo.get_user_episode_playlist(user)
    assert len(episode_playlist) == 1

def test_repository_can_get_playlist_total(database_repo):
    user = database_repo.get_user('thorke')
    if user is None:
        user = User(1, 'thorke', 'password')
        database_repo.add_user(user)

    episode = database_repo.get_episode(1, 1)
    podcast = database_repo.get_podcast(1)

    database_repo.add_to_user_playlist(user, episode)
    database_repo.add_to_user_playlist(user, podcast)

    playlist = database_repo.get_user_playlist(user)
    playlist_total = database_repo.get_playlist_total(user)

    assert playlist_total == 2