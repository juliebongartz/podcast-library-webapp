from podcast.adapters.repository import AbstractRepository
from typing import Iterable
from podcast.domainmodel.model import Podcast

def search_podcasts(repo: AbstractRepository, search_term: str, search_filter: str):
    return podcasts_to_dict(repo.search_podcasts(search_term, search_filter))

def podcast_to_dict(podcast: Podcast):
    podcast_dict = {
        'podcast_id': podcast.id,
        'title': podcast.title,
        'author':  podcast.author,
        'image': podcast.image,
        'description': podcast.description,
        'language': podcast.language,
        'website': podcast.website,
        'itunes': podcast.itunes_id,
        'categories': podcast.categories
    }
    return podcast_dict

def podcasts_to_dict(podcasts: Iterable[Podcast]):
    return [podcast_to_dict(podcast) for podcast in podcasts]

def get_number_of_podcasts(results: list):
    return len(results)
def get_maximum_width(results: list):
    return (100 / 5) * len(results)