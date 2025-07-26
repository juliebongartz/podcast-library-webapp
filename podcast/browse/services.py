from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_number_of_podcasts(repo: AbstractRepository):
    return repo.get_number_of_podcasts()

def get_podcasts(repo: AbstractRepository):
    podcasts = repo.get_podcasts()
    podcast_dicts = []

    for podcast in podcasts:
        category_names = [category.name for category in podcast.categories]
        podcast_dict = {
            'id': podcast.id,
            'title': podcast.title,
            'author':  podcast.author,
            'image': podcast.image,
            'description': podcast.description,
            'language': podcast.language,
            'website': podcast.website,
            'itunes': podcast.itunes_id,
            'categories': category_names
        }
        podcast_dicts.append(podcast_dict)
    return podcast_dicts