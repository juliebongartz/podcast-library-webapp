import pytest

from flask import session

from podcast import create_app
from utils import get_project_root

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login' #localhost


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))


def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

# FAILING
def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'

#FAILING
def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Podcast Library' in response.data


def test_login_required_to_review(client):
    response = client.post('/review_podcast')
    assert response.headers['Location'] == '/authentication/login' #http://localhost

#FAILING
def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review_podcast?podcast_id=2')
    assert response.status_code == 200

    # Check that the page reroutes to podcast page when review is left.
    response = client.post(
        '/review_podcast',
        data={'comment': 'Who is this?', 'podcast_id': 2, 'rating': 5}
    )

    assert response.status_code == 302
    assert response.headers['Location'] == '/show_description/2'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Hey', (b'Your comment is too short')),
))

#FAILING
def test_review_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review_podcast',
        data={'comment': comment, 'podcast_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_podcasts_with_comment(client):
    # Check that we can retrieve the articles page.
    response = client.get('/show_description/1?view_reviews_for=1')
    assert response.status_code == 200

    # Check that all comments for specified article are included on the page.
    assert b'Oh noooo!' in response.data
    assert b'Yeahhhh!!' in response.data


