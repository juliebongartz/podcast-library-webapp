from flask import Blueprint, render_template, redirect, url_for, flash, session
from podcast.authentication.authentication import login_required
import podcast.playlist.services as services
import podcast.adapters.repository as repo

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/add_to_playlist/<int:podcast_id>/<int:episode_id>')
@login_required
def add_to_playlist(podcast_id, episode_id):
    if 'user_name' not in session or session['user_name'] is None:
        flash('Session expired or invalid. Please register or log in again.', 'warning')
        return redirect(url_for('authentication_bp.register'))

    item = services.get_item(podcast_id, episode_id)
    if item:
        services.add_to_user_playlist(session['user_name'], item)
        flash(f"'{ item.title }' has been added to your playlist!", 'success')
    return redirect(url_for('show_bp.show', podcast_id=podcast_id))

@playlist_bp.route('/remove_from_playlist/<int:podcast_id>/<int:episode_id>')
@login_required
def remove_from_playlist(podcast_id, episode_id):
    if 'user_name' not in session or session['user_name'] is None:
        flash('Session expired or invalid. Please register or log in again.', 'warning')
        return redirect(url_for('authentication_bp.register'))

    item = services.get_item(podcast_id, episode_id)
    if item:
        services.remove_from_user_playlist(session['user_name'], item)
        flash(f"'{ item.title }' has been removed from your playlist!", 'info')

    return redirect(url_for('show_bp.show', podcast_id=podcast_id))

@playlist_bp.route('/my_playlist')
@login_required
def view_playlist():
    # Check if session contains user_name and if the user exists in the repository
    if 'user_name' not in session or session['user_name'] is None:
        flash('Session expired or invalid. Please log in or register.', 'warning')
        return redirect(url_for('authentication_bp.register'))

    user_name = session['user_name']

    user = repo.repo_instance.get_user(user_name)
    if user is None:
        flash('User not found. Please log in again.', 'warning')
        session.clear()
        return redirect(url_for('authentication_bp.login'))

    podcast_playlist = services.get_user_podcast_playlist(user_name)
    episode_playlist = services.get_user_episode_playlist(user_name)

    session['history'] = url_for('playlist.view_playlist')

    return render_template(
        'playlist.html',
        user_name=user_name,
        podcast_playlist=podcast_playlist,
        episode_playlist=episode_playlist,
        num_podcasts=len(podcast_playlist),
        num_episodes=len(episode_playlist)
    )