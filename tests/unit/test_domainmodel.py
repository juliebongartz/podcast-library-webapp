###CONFTEST

import pytest

from podcast import create_app
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the podcast/adapters/data folder
# tests are written against the csv files in tests, this data path is used to override default path for testing
DATA_PATH = get_project_root() / "podcast" / "adapters" / "data"

def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "Brian Denny"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "Jackson Mumey"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[Doctor Squee, Jesmond Parish Church, USA Radio]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[Jesmond Parish Church, USA Radio]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "USA Radio"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "Comedy"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "Christianity"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)

@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast, "http://audio-link.com", 3600, "First Episode", "Description", "2024-08-21")

@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user, "My Playlist")

def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1

def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "shyamli"
    assert repr(user2) == "asma"
    assert repr(user3) == "jenny"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"

def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "shyamli"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes

def test_episode_initialization(my_podcast):
    episode = Episode(1, my_podcast, "http://audio-link.com", 3600, "First Episode", "Description", "2024-08-21")
    assert episode.id == 1
    assert episode.podcast == my_podcast
    assert episode.audio_link == "http://audio-link.com"
    assert episode.audio_length == 3600
    assert episode.title == "First Episode"
    assert episode.description == "Description"
    assert episode.publish_date == "2024-08-21"

    # Test invalid initialization
    with pytest.raises(ValueError):
        Episode(-1, my_podcast, "http://audio-link.com", 3600)
    with pytest.raises(ValueError):
        Episode(1, my_podcast, "", 3600)
    with pytest.raises(ValueError):
        Episode(1, my_podcast, "http://audio-link.com", -1)

def test_episode_title_setter(my_episode):
    my_episode.title = "Updated Title"
    assert my_episode.title == "Updated Title"

    with pytest.raises(ValueError):
        my_episode.title = ""

def test_episode_audio_link_setter(my_episode):
    my_episode.audio_link = "http://new-audio-link.com"
    assert my_episode.audio_link == "http://new-audio-link.com"

    with pytest.raises(ValueError):
        my_episode.audio_link = ""

def test_episode_audio_length_setter(my_episode):
    my_episode.audio_length = 4000
    assert my_episode.audio_length == 4000

    with pytest.raises(ValueError):
        my_episode.audio_length = -10

def test_episode_description_setter(my_episode):
    my_episode.description = "Updated Description"
    assert my_episode.description == "Updated Description"

    with pytest.raises(ValueError):
        my_episode.description = ""

def test_episode_publish_date_setter(my_episode):
    my_episode.publish_date = "2024-08-22"
    assert my_episode.publish_date == "2024-08-22"

    with pytest.raises(ValueError):
        my_episode.publish_date = ""

def test_episode_eq():
    author = Author(1, "John Doe")
    podcast = Podcast(100, author, "Test Podcast")
    episode1 = Episode(1, podcast, "http://audio-link.com", 3600, "First Episode")
    episode2 = Episode(1, podcast, "http://audio-link.com", 3600, "First Episode")
    episode3 = Episode(2, podcast, "http://audio-link.com", 3600, "Second Episode")

    assert episode1 == episode2
    assert episode1 != episode3

def test_episode_hash():
    author = Author(1, "John Doe")
    podcast = Podcast(100, author, "Test Podcast")
    episode1 = Episode(1, podcast, "http://audio-link.com", 3600, "First Episode")
    episode2 = Episode(1, podcast, "http://audio-link.com", 3600, "First Episode")
    episode3 = Episode(2, podcast, "http://audio-link.com", 3600, "Second Episode")

    episode_set = {episode1, episode2, episode3}
    assert len(episode_set) == 2  # Since episode1 and episode2 have the same ID

def test_episode_lt():
    author = Author(1, "John Doe")
    podcast = Podcast(100, author, "Test Podcast")
    episode1 = Episode(1, podcast, "http://audio-link.com", 3600, "First Episode")
    episode2 = Episode(2, podcast, "http://audio-link.com", 3600, "Second Episode")

    assert episode1 < episode2

    episode_list = [episode2, episode1]
    assert sorted(episode_list) == [episode1, episode2]


def test_review_initialization():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    assert review.poster == user
    assert review.podcast == podcast
    assert review.rating == 5
    assert review.comment == "Great podcast!"


#def test_invalid_review_id():
    #user = User(1, "John Doe", "securepassword")
    #podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    #with pytest.raises(ValueError):
        #Review(-1, user, podcast, 5, "Great podcast!")

def test_invalid_poster_type():
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    with pytest.raises(TypeError):
        Review(1, "Not a User object", podcast, 5, "Great podcast!")

def test_invalid_podcast_type():
    user = User(1, "John Doe", "securepassword")
    with pytest.raises(TypeError):
        Review(1, user, "Not a Podcast object", 5, "Great podcast!")


def test_invalid_rating():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    with pytest.raises(ValueError):
        Review(user, podcast, -1, "Great podcast!")


def test_set_poster():
    user1 = User(1, "John Doe", "securepassword1")
    user2 = User(2, "Jane Doe", "securepassword2")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user1, podcast, 5, "Great podcast!")

    review.poster = user2
    assert review.poster == user2


def test_set_invalid_poster():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    with pytest.raises(TypeError):
        review.poster = "Not a User object"


def test_set_podcast():
    user = User(1, "John Doe", "securepassword")
    podcast1 = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    podcast2 = Podcast(101, Author(2, "John Smith"), "Another Podcast")
    review = Review( user, podcast1, 5, "Great podcast!")

    review.podcast = podcast2
    assert review.podcast == podcast2


def test_set_invalid_podcast():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    with pytest.raises(TypeError):
        review.podcast = "Not a Podcast object"


def test_set_rating():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    review.rating = 4
    assert review.rating == 4


def test_set_invalid_rating():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    with pytest.raises(ValueError):
        review.rating = -1


def test_set_comment():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    review.comment = "Updated comment"
    assert review.comment == "Updated comment"


def test_set_invalid_comment():
    user = User(1, "John Doe", "securepassword")
    podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    review = Review( user, podcast, 5, "Great podcast!")

    with pytest.raises(ValueError):
        review.comment = ""

#def test_review_equality():
    #user = User(1, "John Doe", "securepassword")
    #podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    #review1 = Review(1, user, podcast, 5, "Great podcast!")
    #review2 = Review(1, user, podcast, 5, "Great podcast!")
    #review3 = Review(2, user, podcast, 4, "Good podcast!")

    #assert review1 == review2
    #assert review1 != review3

#def test_review_hash():
    #user = User(1, "John Doe", "securepassword")
    #podcast = Podcast(100, Author(1, "Jane Smith"), "Test Podcast")
    #review1 = Review( user, podcast, 5, "Great podcast!")
    #review2 = Review( user, podcast, 5, "Great podcast!")
    #review3 = Review( user, podcast, 4, "Good podcast!")

    #review_set = {review1, review2, review3}
    #assert len(review_set) == 2

def test_playlist_initialization(my_user):
    playlist = Playlist(1, my_user, "My Playlist")
    assert playlist.id == 1
    assert playlist.creator == my_user
    assert playlist.name == "My Playlist"
    assert playlist._episode_list == []

def test_playlist_name_setter(my_playlist):
    my_playlist.name = "New Playlist Name"
    assert my_playlist.name == "New Playlist Name"

    my_playlist.name = "Another Playlist"
    assert my_playlist.name == "Another Playlist"

def test_playlist_creator_setter(my_playlist, my_user):
    new_user = User(2, "Jane Doe", "password456")
    my_playlist.creator = new_user
    assert my_playlist.creator == new_user

    with pytest.raises(TypeError):
        my_playlist.creator = "not a user"

def test_playlist_add_episode(my_playlist, my_episode):
    my_playlist.add_item(my_episode)

    assert my_episode in my_playlist._episode_list
    assert len(my_playlist._episode_list) == 1

    with pytest.raises(TypeError):
        my_playlist.add_item("not an episode")

def test_playlist_remove_episode(my_playlist, my_episode):
    my_playlist.add_item(my_episode)
    my_playlist.remove_item(my_episode)
    assert my_episode not in my_playlist._episode_list

    my_playlist.remove_item(my_episode)
    assert len(my_playlist._episode_list) == 0

def test_playlist_remove_non_existent_episode(my_playlist, my_episode):
    my_playlist.remove_item(my_episode)
    assert len(my_playlist._episode_list) == 0


def test_playlist_eq(my_user):
    playlist1 = Playlist(1, my_user, "Playlist One")
    playlist2 = Playlist(1, my_user, "Playlist One")
    playlist3 = Playlist(2, my_user, "Playlist Two")

    assert playlist1 == playlist2
    assert playlist1 != playlist3
    assert playlist2 != playlist3
    assert playlist1 == playlist1
    assert playlist1 != "Not a Playlist"

def test_playlist_hash(my_user):
    playlist1 = Playlist(1, my_user, "Playlist One")
    playlist2 = Playlist(1, my_user, "Playlist One")
    playlist3 = Playlist(2, my_user, "Playlist Two")

    playlist_set = {playlist1, playlist2, playlist3}
    assert len(playlist_set) == 2

def test_read_podcasts():
    csvdatareader = CSVDataReader()
    csvdatareader.read_podcasts(DATA_PATH)
    assert len(csvdatareader.dataset_of_podcasts) == 1000;

def test_podcast_ids():
    csvdatareader = CSVDataReader()
    csvdatareader.read_podcasts(DATA_PATH)

    print(csvdatareader.dataset_of_podcasts[13])
    assert csvdatareader.dataset_of_podcasts[13].id == 14

def test_read_episodes():
    csvdatareader = CSVDataReader()
    csvdatareader.read_podcasts(DATA_PATH)
    csvdatareader.read_episodes(DATA_PATH)

    assert len(csvdatareader.dataset_of_episodes) == 5633;


def test_database_of_podcasts():
    csvdatareader = CSVDataReader()
    csvdatareader.read_podcasts(DATA_PATH)
    csvdatareader.read_episodes(DATA_PATH)

    assert isinstance(csvdatareader.dataset_of_podcasts[13], Podcast)

def test_get_author():
    csvdatareader = CSVDataReader()
    csvdatareader.read_podcasts(DATA_PATH)
    csvdatareader.read_episodes(DATA_PATH)