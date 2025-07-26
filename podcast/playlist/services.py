from podcast.adapters.repository import repo_instance
from podcast.domainmodel.model import Podcast, Episode

def get_podcast(podcast_id: int):
    """Retrieve a podcast by its ID."""
    return repo_instance.get_podcast(podcast_id)

def get_item(podcast_id: int, episode_id: int):
    if episode_id is not 0:
        return repo_instance.get_episode(podcast_id, episode_id)
    return repo_instance.get_podcast(podcast_id)

def add_to_user_playlist(user_name: str, item: Podcast | Episode):
    user = repo_instance.get_user(user_name)
    return repo_instance.add_to_user_playlist(user, item)

def remove_from_user_playlist(user_name: str, item: Podcast | Episode):
    user = repo_instance.get_user(user_name)
    return repo_instance.remove_from_user_playlist(user, item)

def get_user_playlist_details(user_name: str):
    """Retrieve the playlist for a specific user."""
    user = repo_instance.get_user(user_name)
    playlist = repo_instance.get_user_playlist(user)

    playlist_dict = {
        'username': user_name,
        'title': playlist.name,
        'total': repo_instance.get_playlist_total(playlist)
    }

    return playlist_dict

def get_user_podcast_playlist(user_name: str):
    user = repo_instance.get_user(user_name)
    playlist = repo_instance.get_user_podcast_playlist(user)
    podcasts_dict = []

    for podcast in playlist:
        podcast_dict = {
            'id': podcast.id,
            'title': podcast.title,
            'author': podcast.author,
            'image': podcast.image,
        }
        podcasts_dict.append(podcast_dict)

    return podcasts_dict

def get_user_episode_playlist(user_name: str):
    user = repo_instance.get_user(user_name)
    playlist = repo_instance.get_user_episode_playlist(user)
    episodes_dict = []

    for episode in playlist:
        episode_dict = {
            'id': episode.id,
            'title': episode.title,
            'author': episode.podcast.author,
            'podcast_id': episode.podcast.id,
            'podcast_title': episode.podcast.title
        }
        episodes_dict.append(episode_dict)

    return episodes_dict
