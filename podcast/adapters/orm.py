from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import registry, relationship

from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Review, Playlist

# global variable giving access to the MetaData (schema) information of the database
# metadata = MetaData()
mapper_registry = registry()

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

author_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True), #autoincrement=True),
    Column('name', String(255)) #nullable=False)
)

episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('audio', String(255), nullable=False),
    Column('audio_length', Integer, nullable=False),
    Column('description', Text, nullable=True),
    Column('pub_date', String(64), nullable=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id'))
)

category_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64), nullable=False)
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True), #autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('rating', Integer, nullable=False),
    Column('comment', Text, nullable=True)
)

playlist_table = Table(
    'playlists', mapper_registry.metadata,
    Column('id', Integer, primary_key=True), #, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'))
)

podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

playlist_podcasts_table = Table(
    'playlist_podcasts', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('playlist_id', ForeignKey('playlists.id'))
)

playlist_episodes_table = Table(
    'playlist_episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('episode_id', ForeignKey('episodes.id')),
    Column('playlist_id', ForeignKey('playlists.id'))
)

def map_model_to_tables():
    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.id,
        '_username': users_table.c.user_name,
        '_password': users_table.c.password,
        '_reviews': relationship(Review),
        '_playlist': relationship(Playlist, uselist=False)
    })
    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author, back_populates='_podcast_list'),
        '_reviews': relationship(Review, back_populates='podcast'),
        'episodes': relationship(Episode, back_populates='podcast'),
        'categories': relationship(Category, secondary=podcast_categories_table),
    })
    mapper_registry.map_imperatively(Author, author_table, properties={
        '_id': author_table.c.author_id,
        '_name': author_table.c.name,
        '_podcast_list': relationship(Podcast, back_populates='_author')  # Not sure about this
    })
    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_id': episode_table.c.id,
        '_title': episode_table.c.title,
        '_audio_link': episode_table.c.audio,
        '_audio_length': episode_table.c.audio_length,
        '_description': episode_table.c.description,
        '_audio_length': episode_table.c.audio_length,
        '_description': episode_table.c.description,
        '_publish_date': episode_table.c.pub_date,
        'podcast': relationship(Podcast, back_populates='episodes')
    })
    mapper_registry.map_imperatively(Category, category_table, properties={
        '_id': category_table.c.category_id,
        '_name': category_table.c.category_name,
        'podcasts': relationship(Podcast, secondary=podcast_categories_table, back_populates='categories')
    })
    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_id': reviews_table.c.id,
        '_rating': reviews_table.c.rating,
        '_comment': reviews_table.c.comment,
        '_poster': relationship(User, back_populates='_reviews'),
        'podcast': relationship(Podcast, back_populates='_reviews')
    })
    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_id' : playlist_table.c.id,
        '_name': playlist_table.c.name,
        '_creator': relationship(User, back_populates='_playlist'),
        '_podcast_list': relationship(Podcast, secondary=playlist_podcasts_table),
        '_episode_list': relationship(Episode, secondary=playlist_episodes_table),
    })