from flask import Blueprint, render_template, request, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

import podcast.adapters.repository as repo
import podcast.show_description.services as services
from podcast.authentication.authentication import login_required

show_blueprint = Blueprint('show_bp', __name__)

@show_blueprint.route('/show_description/<int:podcast_id>', methods=['GET'])
def show(podcast_id):
    podcast = services.get_podcast(repo.repo_instance, podcast_id)
    podcast_dict = services.podcast_to_dict(podcast)
    podcast_to_show_reviews = request.args.get('view_reviews_for')

    if podcast_to_show_reviews is None:
        podcast_to_show_reviews = -1
    else:
        try:
            podcast_to_show_reviews = int(podcast_to_show_reviews)
        except ValueError:
            podcast_to_show_reviews = -1
    
    episodes_per_page = 3

    episode_cursor = request.args.get('cursor')

    if episode_cursor is None:
        # Cursor starts at beginning
        episode_cursor = 0
    else:
        # Convert string cursor to int
        episode_cursor = int(episode_cursor)

    num_episodes = services.get_number_of_episodes(repo.repo_instance, podcast)
    all_episodes = services.get_episodes(repo.repo_instance, podcast)

    # Episodes to show on this page
    episodes = all_episodes[episode_cursor : episode_cursor + episodes_per_page]

    first_episode_url = None
    last_episode_url = None
    next_episode_url = None
    prev_episode_url = None

    if episode_cursor > 0:
        # There are podcasts before
        prev_episode_url = url_for('show_bp.show', podcast_id=podcast_id, cursor=episode_cursor - episodes_per_page)
        first_episode_url = url_for('show_bp.show', podcast_id=podcast_id)

    if episode_cursor + episodes_per_page < num_episodes:
        # There are next and last podcasts
        next_episode_url = url_for('show_bp.show', podcast_id=podcast_id, cursor=episode_cursor + episodes_per_page)

        last_cursor = episodes_per_page * int(num_episodes / episodes_per_page)
        if num_episodes % episodes_per_page == 0:
            last_cursor -= episodes_per_page
        last_episode_url = url_for('show_bp.show', podcast_id=podcast_id, cursor=last_cursor)

    # Construct urls for viewing podcast reviews and adding reviews.
    podcast_dict['view_review_url'] = url_for('show_bp.show', podcast_id=podcast_id, view_reviews_for=podcast_dict['id'])
    #view_reviews_url = url_for('show_bp.show', podcast_id=podcast_id)
    add_review_url = url_for('show_bp.review_podcast', podcast_id=podcast_id)

    user_in_session = False
    user_podcast_playlist = []
    user_episode_playlist = []

    if 'user_name' in session and repo.repo_instance.get_user(session['user_name']):
        user_in_session = True
        user_podcast_playlist = services.get_user_podcast_playlist(repo.repo_instance, session['user_name'])
        user_episode_playlist = services.get_user_episode_playlist(repo.repo_instance, session['user_name'])

    if 'user_name' in session and not repo.repo_instance.get_user(session['user_name']):
        session.pop('user_name', None)

    print("Podcast to show reviews",podcast_to_show_reviews)

    return render_template(
        'podcastDescription.html',
        title='Episodes',
        podcast=podcast,
        podcast_dict=podcast_dict,
        episodes=episodes,
        number_of_episodes=num_episodes,
        first_episode_url=first_episode_url,
        last_episode_url=last_episode_url,
        prev_episode_url=prev_episode_url,
        next_episode_url=next_episode_url,
        episode_length_to_min=services.episode_length_to_min,
        show_reviews_for_podcast=podcast_to_show_reviews,
        add_review_url=add_review_url,
        user_in_session=user_in_session,
        user_podcast_playlist=user_podcast_playlist,
        user_episode_playlist=user_episode_playlist
    )


@show_blueprint.route('/review_podcast', methods=['GET', 'POST'])
@login_required
def review_podcast():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the podcast id, representing the commented article, from the form.
        podcast_id = int(form.podcast_id.data)

        # Use the service layer to store the new comment.
        services.add_review(podcast_id, form.comment.data, user_name, form.rating.data, repo.repo_instance)

        # Retrieve the article in dict form.
        podcast = services.get_podcast(repo.repo_instance, podcast_id)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('show_bp.show', podcast_id=podcast_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form. Extract the article id, representing the article to comment, from a query parameter of the GET request.
        podcast_id = int(request.args.get('podcast_id'))

        # Store the article id in the form.
        form.podcast_id.data = podcast_id
    else:
        # Request is a HTTP POST where form validation has failed. Extract the article id of the article being commented from the form.
        podcast_id = int(form.podcast_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    podcast = services.get_podcast(repo.repo_instance, podcast_id)

    return render_template(
        'review_podcast.html',
        title='Edit podcast',
        podcast=podcast,
        form=form,
        handler_url=url_for('show_bp.review_podcast')
    )


class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short')])
    rating = IntegerField('Rating', [DataRequired(), NumberRange(min=1, max=5)])
    podcast_id = HiddenField("Podcast id")
    submit = SubmitField('Submit')

