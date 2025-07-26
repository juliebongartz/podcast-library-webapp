from flask import Blueprint, render_template, request, url_for, session

import podcast.adapters.repository as repo
import podcast.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    podcasts_per_page = 10

    cursor = request.args.get('cursor')

    if cursor is None:
        # Cursor starts at beginning
        cursor = 0
    else:
        # Convert string cursor to int
        cursor = int(cursor)

    num_podcasts = services.get_number_of_podcasts(repo.repo_instance)
    all_podcasts = services.get_podcasts(repo.repo_instance)

    # Podcasts to show on this page
    podcasts = all_podcasts[cursor : cursor + podcasts_per_page]

    # Ensure each podcast has a unique podcast_id that considers the cursor
    for i, podcast in enumerate(podcasts):
        podcast['podcast_id'] = cursor + i+1

    first_podcast_url = None
    last_podcast_url = None
    next_podcast_url = None
    prev_podcast_url = None

    if cursor > 0:
        # There are podcasts before
        prev_podcast_url = url_for('browse_bp.browse', cursor=cursor - podcasts_per_page)
        first_podcast_url = url_for('browse_bp.browse')

    if cursor + podcasts_per_page < num_podcasts:
        # There are next and last podcasts
        next_podcast_url = url_for('browse_bp.browse', cursor=cursor + podcasts_per_page)

        last_cursor = podcasts_per_page * int(num_podcasts / podcasts_per_page)
        if num_podcasts % podcasts_per_page == 0:
            last_cursor -= podcasts_per_page
        last_podcast_url = url_for('browse_bp.browse', cursor=last_cursor)

    session['history'] = url_for('browse_bp.browse', cursor=cursor)

    return render_template(
        '/catalogue.html',
        title='Podcast Catalogue',
        podcasts=podcasts,
        first_podcast_url=first_podcast_url,
        last_podcast_url=last_podcast_url,
        prev_podcast_url=prev_podcast_url,
        next_podcast_url=next_podcast_url,
        cursor=cursor,
        number_of_podcasts=num_podcasts
    )