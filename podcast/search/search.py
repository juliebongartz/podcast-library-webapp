from flask import Blueprint, render_template, request, url_for, session
import podcast.adapters.repository as repo
import podcast.search.services as services

search_blueprint = Blueprint('search_bp', __name__)

@search_blueprint.route('/search', methods=['GET'])
def search():
    podcasts_per_page = 10

    search_term = request.args.get('search_term', '')
    search_filter = request.args.get('search_filter', 'title')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    results = services.search_podcasts(repo.repo_instance, search_term, search_filter)
    number_of_podcasts = services.get_number_of_podcasts(results)
    maximum_width = services.get_maximum_width(results)

    results = results[cursor : cursor + podcasts_per_page]

    first_podcast_url = None
    last_podcast_url = None
    next_podcast_url = None
    prev_podcast_url = None

    if cursor > 0:
        prev_podcast_url = url_for('search_bp.search', search_term=search_term, search_filter=search_filter, cursor=cursor - podcasts_per_page)
        first_podcast_url = url_for('search_bp.search', search_term=search_term, search_filter=search_filter)

    if cursor + podcasts_per_page < number_of_podcasts:
        next_podcast_url = url_for('search_bp.search', search_term=search_term, search_filter=search_filter, cursor=cursor + podcasts_per_page)

        last_cursor = podcasts_per_page * int(number_of_podcasts / podcasts_per_page)
        if number_of_podcasts % podcasts_per_page == 0:
            last_cursor -= podcasts_per_page
        last_podcast_url = url_for('search_bp.search', search_term=search_term, search_filter=search_filter, cursor=last_cursor)

    title = f"Showing {number_of_podcasts} search results for '{search_term}' in {search_filter}"

    session['history'] = url_for('search_bp.search', search_term=search_term, search_filter=search_filter, cursor=cursor)

    return render_template(
        '/catalogue.html',
        title=title,
        podcasts=results,
        first_podcast_url=first_podcast_url,
        last_podcast_url=last_podcast_url,
        next_podcast_url=next_podcast_url,
        prev_podcast_url=prev_podcast_url,
        cursor=cursor,
        number_of_podcasts=number_of_podcasts,
        maximum_width=maximum_width
    )