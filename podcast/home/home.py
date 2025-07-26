from flask import Blueprint, render_template, session, url_for
import podcast.adapters.repository as repo
import podcast.home.services as services

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    featured = services.featured_podcasts(repo.repo_instance)
    session['history'] = url_for('home_bp.home')
    return render_template('/layout.html', podcasts=featured)