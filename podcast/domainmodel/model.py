from __future__ import annotations
from typing import List, Iterable


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self._reviews: List[Review] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self._reviews)

    @property
    def number_of_reviews(self) -> int:
        return len(self._reviews)

    def add_review(self, review: Review):
        self._reviews.append(review)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()
        self.podcasts: List[Podcast] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"{self._name}"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._username = username.lower().strip()
        self._id = user_id
        self._password = password
        self._subscription_list = []
        self._reviews: List[Review] = list()
        self._playlist = Playlist(user_id, self, f"{self._username}'s Playlist")

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    @property
    def playlist(self):
        return self._playlist

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def __repr__(self):
        return self.username

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


# Self-defined classes:
class Episode:
    def __init__(self, episode_id: int, podcast: Podcast, audio_link: str, audio_length: int,
                 title: str = "Untitled", description: str = "", publish_date: str = "Undated"):
        validate_non_negative_int(episode_id)
        validate_non_empty_string(audio_link)
        validate_non_negative_int(audio_length)
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = episode_id
        self._podcast = podcast
        self._title = title
        self._audio_link = audio_link
        self._audio_length = audio_length
        self._description = description
        self._publish_date = publish_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self._title = new_title

    @property
    def audio_link(self):
        return self._audio_link

    @audio_link.setter
    def audio_link(self, new_audio_link: str):
        validate_non_empty_string(new_audio_link, "Episode audio link")
        self._audio_link = new_audio_link

    @property
    def audio_length(self):
        return self._audio_length

    @audio_length.setter
    def audio_length(self, new_audio_length: int):
        validate_non_negative_int(new_audio_length)
        self._audio_length = new_audio_length

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        validate_non_empty_string(new_description, "Episode description")
        self._description = new_description

    @property
    def publish_date(self):
        return self._publish_date

    @publish_date.setter
    def publish_date(self, new_publish_date: str):
        validate_non_empty_string(new_publish_date, "Episode publish date")
        self._publish_date = new_publish_date

    def __repr__(self):
        return self._title

    def __eq__(self, other):
        if isinstance(other, Episode):
            return self._id == other._id
        return False

    def __hash__(self):
        return hash(self._id)

    def __lt__(self, other):
        if isinstance(other, Episode):
            return self._id < other._id
        return NotImplemented

class Review:
    def __init__(self, poster: User, podcast: Podcast, rating: int, comment: str = "No comment"): #removed id
        if poster is None or not isinstance(poster, User):
            raise TypeError("Poster must be a User object and cannot be None.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        validate_non_negative_int(rating)
        #self._id = review_id
        self._poster = poster
        self._podcast = podcast
        self._rating = rating
        self._comment = comment

    #@property
    #def id(self) -> int:
        #return self._id

    @property
    def poster(self) -> User:
        return self._poster

    @poster.setter
    def poster(self, new_poster: User):
        if not isinstance(new_poster, User):
            raise TypeError("Poster must be a User object.")
        self._poster = new_poster

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, new_rating: int):
        validate_non_negative_int(new_rating)
        self._rating = new_rating

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, new_comment: str):
        validate_non_empty_string(new_comment, "Review comment")
        self._comment = new_comment

    #def __eq__(self, other):
        #if isinstance(other, Review):
            #return self._id == other._id
        #return False

    #def __hash__(self):
        #return hash(self._id)

    def __repr__(self):
        return self._comment

    def __lt__(self, other):
        if isinstance(other, Review):
            return self._rating < other._rating
        return NotImplemented

class Playlist:
    def __init__(self, playlist_id: int, creator: User, playlist_name: str = "Untitled"):
        validate_non_negative_int(playlist_id)
        if not isinstance(creator, User):
            raise TypeError("Creator must be a User object.")
        self._id = playlist_id
        self._creator = creator
        self._name = playlist_name
        self._episode_list = []
        self._podcast_list: List[Podcast] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def creator(self) -> User:
        return self._creator

    @creator.setter
    def creator(self, new_creator: User):
        if not isinstance(new_creator, User):
            raise TypeError("Creator must be a User object.")
        self._creator = new_creator

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def podcast_list(self):
        return self._podcast_list

    @property
    def episode_list(self):
        return self._episode_list

    def add_item(self, item: Episode | Podcast):
        if isinstance(item, Episode) and item not in self._episode_list:
            self._episode_list.append(item)
            return
        if isinstance(item, Podcast) and item not in self._podcast_list:
            self._podcast_list.append(item)
            return
        raise TypeError("item must be an Episode or Podcast object.")

    def remove_item(self, item: Episode | Podcast):
        if item in self._episode_list:
            self._episode_list.remove(item)
        if item in self._podcast_list:
            self._podcast_list.remove(item)

    def __repr__(self):
        return f"Episodes: {self._episode_list}), Podcasts: {self._podcast_list}"

    def __lt__(self, other):
        if isinstance(other, Playlist):
            return len(self._episode_list) < len(other._episode_list)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Playlist):
            return (self._id == other._id and
                    self._creator == other._creator and
                    self._name == other._name)
        return False

    def __hash__(self):
        return hash((self._id, self._creator, self._name))


def make_review(comment: str, poster: User, podcast: Podcast, rating: int):
    review = Review(poster, podcast, rating, comment)
    poster.add_review(review)
    podcast.add_review(review)

    return review