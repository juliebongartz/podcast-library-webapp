from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    actual_table_names = inspector.get_table_names()
    expected_table_names = ['authors', 'categories', 'episodes', 'playlist_episodes', 'playlist_podcasts', 'playlists',
                            'podcast_categories', 'podcasts', 'reviews', 'users']

    assert actual_table_names == expected_table_names

def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])

def test_database_populate_select_all_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])

def test_database_populate_select_all_podcasts(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])

def test_database_populate_select_all_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])

def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_users_table])