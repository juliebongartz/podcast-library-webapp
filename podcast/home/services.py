from podcast.domainmodel.model import Podcast
from podcast.adapters.repository import AbstractRepository
from podcast.adapters.database_repository import SqlAlchemyRepository

def featured_podcasts(repo: AbstractRepository): #abstract repo
    podcasts = repo.get_podcasts()
    featured = [636, 431, 171, 392, 915]
    featured_list = []
    for feature in featured:
        for podcast in podcasts:
            if feature == podcast.id:
                featured_list.append(podcast)
    return featured_list