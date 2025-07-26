import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from podcast.domainmodel.model import User, Podcast, Episode, Review, make_review, Author

def insert_user(empty_session, values=None):
    new_name = "andrew"
    new_password = "andrew"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    # Wrap the SQL string in text()
    empty_session.execute(
        text('INSERT INTO users (user_name, password) VALUES (:user_name, :password)'),
        {'user_name': new_name, 'password': new_password}
    )

    row = empty_session.execute(
        text('SELECT id from users where user_name = :user_name'),
        {'user_name': new_name}
    ).fetchone()

    return row[0]

def insert_users(empty_session, values):
    for value in values:
        # Wrap the SQL string in text()
        empty_session.execute(
            text('INSERT INTO users (user_name, password) VALUES (:user_name, :password)'),
            {'user_name': value[0], 'password': value[1]}
        )
    rows = list(empty_session.execute(text('SELECT id from users')))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_podcast(empty_session):
    # Wrap the SQL string in text()
    empty_session.execute(
        text('INSERT INTO podcasts (title, image_url, description, language, website, author_id) VALUES '
             '(:title, :image_url, :description, :language, :website, :author_id)'),
        {
            'title': "Podcast Title",
            'image_url': "http://example.com/image.jpg",
            'description': "Description of the podcast.",
            'language': "English",
            'website': "http://example.com",
            'author_id': 1
        }
    )
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]

def insert_episode(empty_session, podcast_id):
    # Wrap the SQL string in text()
    empty_session.execute(
        text('INSERT INTO episodes (title, audio, audio_length, description, pub_date, podcast_id) VALUES '
             '(:title, :audio, :audio_length, :description, :pub_date, :podcast_id)'),
        {
            'title': "Episode Title",
            'audio': "http://example.com/audio.mp3",
            'audio_length': 3600,
            'description': "Description of the episode.",
            'pub_date': "2024-01-01",
            'podcast_id': podcast_id
        }
    )
    row = empty_session.execute(text('SELECT id from episodes')).fetchone()
    return row[0]

def insert_review(empty_session, user_id, podcast_id):
    # Wrap the SQL string in text()
    empty_session.execute(
        text('INSERT INTO reviews (user_id, podcast_id, rating, comment) VALUES (:user_id, :podcast_id, 5, "Great podcast!")'),
        {'user_id': user_id, 'podcast_id': podcast_id}
    )

def make_user(user_id=1, username="andrew", password="111"):
    return User(user_id, username, password)

def make_podcast():
    author = Author(author_id=1, name="Author Name")  # Replace with how you create an Author
    return Podcast(
        podcast_id=1,  # You can set a fixed ID for testing; ensure it's unique
        author=author,
        title="Podcast Title",
        image=None,  # Set this to None or provide an image string
        description="Description of the podcast.",
        language="English",
        website="http://example.com",
        itunes_id=None,  # Set as needed
    )

def test_loading_of_users(empty_session):
    users = [("andrew", "1234"), ("Cindy", "1111")]
    user_ids = [insert_user(empty_session, user) for user in users]  # Insert users and get their IDs
    expected = [User(user_ids[0], "andrew", "1234"), User(user_ids[1], "Cindy", "1111")]

    # Retrieve users from the database for comparison
    retrieved_users = [
        User(row[0], row[1], row[2]) for row in
        empty_session.execute(text('SELECT id, user_name, password FROM users')).fetchall()
    ]

    assert expected == retrieved_users

def test_saving_of_users(empty_session):
    user = make_user()
    # Add logic to save the user to the session if needed, e.g.:
    empty_session.add(user)
    empty_session.commit()

    # Verify that the user was saved correctly
    saved_user = empty_session.execute(
        text('SELECT id, user_name, password FROM users WHERE user_name = :username'),
        {'username': user.username}
    ).fetchone()

    expected = User(saved_user[0], saved_user[1], saved_user[2])
    assert user == expected

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("andrew", "1234"))
    empty_session.commit()

    user = User(user_id=0, username="andrew", password="111")
    empty_session.add(user)

    with pytest.raises(IntegrityError):
        empty_session.commit()

def test_loading_of_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    fetched_podcast = empty_session.query(Podcast).one()

    assert fetched_podcast.title == "Podcast Title"
    assert podcast_key == fetched_podcast.id

def test_saving_of_podcast(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT title, description FROM podcasts')))
    assert rows == [("Podcast Title", "Description of the podcast.")]

def test_saving_of_episode(empty_session):
    podcast_key = insert_podcast(empty_session)
    episode_key = insert_episode(empty_session, podcast_key)

    fetched_episode = empty_session.query(Episode).get(episode_key)
    assert fetched_episode.title == "Episode Title"
    assert fetched_episode.podcast_id == podcast_key

def test_saving_of_review(empty_session):
    user_id = insert_user(empty_session, ("andrew", "1234"))
    podcast_id = insert_podcast(empty_session)
    insert_review(empty_session, user_id, podcast_id)

    rows = list(empty_session.execute(text('SELECT user_id, podcast_id, rating, comment FROM reviews')))
    assert rows == [(user_id, podcast_id, 5, "Great podcast!")]