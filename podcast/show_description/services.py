from podcast.adapters.repository import AbstractRepository
from podcast.adapters.repository import repo_instance
from podcast.domainmodel.model import Podcast, make_review, Review, Episode
from typing import List, Iterable


class NonExistentPodcastException(Exception):
    pass

class UnknownUserException(Exception):
    pass

#podcast to dict
def podcast_to_dict(podcast: Podcast):
    article_dict = {
        'id': podcast._id,
        'author': podcast._author,
        'title': podcast._title,
        'image': podcast._image,
        'description': podcast._description,
        'language': podcast._language,
        'website': podcast._website,
        'itunes_id': podcast._itunes_id,
        'categories': podcast.categories,
        'episodes': episodes_to_dict(podcast.episodes),
        'reviews': reviews_to_dict(podcast._reviews)
    }
    return article_dict

def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.poster._username,
        'podcast_id': review.podcast._id,
        'comment': review._comment,
        'rating': review._rating
    }
    return review_dict

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

def episode_to_dict(episode: Episode):
    episode_dict = {
        'id': episode.id,
        'title': episode._title,
        'podcast': episode.podcast,
        'audio_link': episode._audio_link,
        'description': episode._description,
        'audio_length': episode._audio_length,
        'publish_date': episode._publish_date
    }
    return episode_dict

def episodes_to_dict(episodes: Iterable[Episode]):
    return [episode_to_dict(episode) for episode in episodes]


def add_review(podcast_id: int, comment_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the article exists.
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException # need to redirect to login page


    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException #need to redirect to login page


    # Create review
    review = make_review(comment_text, user, podcast, rating)

    # Update the repository.
    repo.add_review(review)


def get_reviews_for_podcast(podcast_id, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    reviews = repo.get_reviews()

    if podcast is None:
        raise NonExistentPodcastException

    review_dicts = []

    for review in reviews:
        review_dict = {
        'username': review._poster._username,
        'podcast': review._podcast,
        'rating': review._rating,
        'comment': review._comment
        }
        if review._podcast._id == podcast_id:
            review_dicts.append(review_dict)

    return review_dicts


def get_podcast(repo: AbstractRepository, podcast_id: int):
    podcasts = repo.get_podcasts()
    for podcast in podcasts:
        if podcast.id == podcast_id:
            return podcast
    return None


def get_number_of_episodes(repo: AbstractRepository, podcast: Podcast):
    return repo.get_number_of_episodes(podcast)


def get_episodes(repo: AbstractRepository, podcast: Podcast):
    episodes = repo.get_episodes(podcast)
    episodes_dicts = []

    for episode in episodes:
        episode_dict = {
            'title': episode.title,
            'description': episode.description,
            'audio_link': episode.audio_link,
            'audio_length': episode.audio_length,
            'publish_date': episode.publish_date,
            'id': episode.id,
        }
        episodes_dicts.append(episode_dict)
    return episodes_dicts

def episode_length_to_min(length: int):
    minutes = length // 60
    seconds = length % 60
    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(minutes) + ":" + str(seconds)

def get_user_podcast_playlist(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name)
    if user is None:
        return []
    playlist = repo.get_user_podcast_playlist(user)
    return [podcast.id for podcast in playlist]

def get_user_episode_playlist(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name)
    if user is None:
        return []
    playlist = repo.get_user_episode_playlist(user)
    return [episode.id for episode in playlist]
