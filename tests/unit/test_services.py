###CONFTEST

import pytest
from werkzeug.security import generate_password_hash, check_password_hash

from podcast import create_app
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.show_description.services import NonExistentPodcastException

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the podcast/adapters/data folder
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

###CONFTEST

import pytest

from podcast.browse import services as browse_services
from podcast.show_description import services as show_description_services
from podcast.home import services as home_services
from podcast.authentication import services as auth_services

# BROWSE

#get_number_of_podcasts
def test_can_get_number_of_podcasts(in_memory_repo):
    assert browse_services.get_number_of_podcasts(in_memory_repo) == 5

#get_podcasts
def test_can_get_podcasts(in_memory_repo):
    podcasts = browse_services.get_podcasts(in_memory_repo)
    assert len(podcasts) == 5


# SHOW DESCRIPTION

#get_podcast
def test_can_get_podcast(in_memory_repo, id=5):
    podcast = show_description_services.get_podcast(in_memory_repo, id)
    assert podcast.title == "Bethel Presbyterian Church (EPC) Sermons"

# get_episodes
def test_can_get_episodes(in_memory_repo):
    podcast = show_description_services.get_podcast(in_memory_repo, 1)
    episodes = show_description_services.get_episodes(in_memory_repo, podcast)
    assert episodes[1]['title'] == "Week 16 Day 5"

# get_number_of_episodes
def test_can_get_episodes_count(in_memory_repo):
    podcast = show_description_services.get_podcast(in_memory_repo, 1)
    assert show_description_services.get_number_of_episodes(in_memory_repo, podcast) == 3


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert check_password_hash(user_as_dict['password'], new_password)

def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)

def test_can_add_review(in_memory_repo):
    podcast_id = 3
    comment_text = 'omg crazy'
    user_name = 'fmercury'

    # Call the service layer to add the comment.
    show_description_services.add_review(podcast_id, comment_text, user_name, 3, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = show_description_services.get_reviews_for_podcast(podcast_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment'] for dictionary in reviews_as_dict if
        dictionary['comment'] == comment_text),
        None) is not None

def test_cannot_add_review_for_non_existent_podcast(in_memory_repo):
    podcast_id = 7
    comment_text = "What's that?"
    user_name = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(show_description_services.NonExistentPodcastException):
            show_description_services.add_review(podcast_id, comment_text, user_name, 2, in_memory_repo)

def test_cannot_add_review_by_unknown_user(in_memory_repo):
    podcast_id = 3
    comment_text = 'omg crazy!'
    user_name = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(show_description_services.UnknownUserException):
        show_description_services.add_review(podcast_id, comment_text, user_name, 4, in_memory_repo)


def test_get_reviews_for_podcast(in_memory_repo):
    reviews_as_dict = show_description_services.get_reviews_for_podcast(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 2

    # Check that the comments relate to the article whose id is 1.
    podcasts = [review['podcast']._id for review in reviews_as_dict]
    podcasts = set(podcasts)

    assert 1 in podcasts and len(podcasts) == 1

def test_get_reviews_for_non_existent_podcast(in_memory_repo):
    with pytest.raises(NonExistentPodcastException):
        reviews_as_dict = show_description_services.get_reviews_for_podcast(7, in_memory_repo)

def test_get_reviews_for_podcast_without_reviews(in_memory_repo):
    reviews_as_dict = show_description_services.get_reviews_for_podcast(3, in_memory_repo)
    assert len(reviews_as_dict) == 0

def test_episode_length_to_min():
    secs = 760
    mins = show_description_services.episode_length_to_min(secs)
    assert mins == "12:40"

def test_can_get_user_podcast_playlist(in_memory_repo):
    user = in_memory_repo.get_user("fmercury")
    podcast = in_memory_repo.get_podcast(1)
    in_memory_repo.add_to_user_playlist(user,podcast)
    assert show_description_services.get_user_podcast_playlist(in_memory_repo,"fmercury") == [1]

def test_can_get_user_episode_playlist(in_memory_repo):
    user = in_memory_repo.get_user("fmercury")
    episode = in_memory_repo.get_episode(1,1)
    in_memory_repo.add_to_user_playlist(user,episode)
    assert show_description_services.get_user_episode_playlist(in_memory_repo,"fmercury") == [1]


# HOME

DATA_PATH = get_project_root() / "podcast" / "adapters" / "data"
@pytest.fixture
def second_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(DATA_PATH, repo)
    return repo

def test_can_get_featured_podcasts(second_memory_repo):
    podcasts = home_services.featured_podcasts(second_memory_repo)
    assert podcasts[2]._title == "Sunny 16"
