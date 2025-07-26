from pathlib import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from utils import get_project_root

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    data_reader = CSVDataReader()

    # Load podcasts and episodes into the repository
    data_reader.read_podcasts(data_path)
    data_reader.read_episodes(data_path)

    if database_mode:
        # Add authors to the repo
        for author in data_reader.dataset_of_authors:
            repo.add_author(author)

        # Add categories to the repo
        for category in data_reader.dataset_of_categories:
            repo.add_category(category)


    for podcast in data_reader.dataset_of_podcasts:
        repo.add_podcast(podcast)

    if database_mode:
        # Add episodes to the repo
        for episode in data_reader.dataset_of_episodes:
            repo.add_episode(episode)

    if data_path == get_project_root() / "tests" / "data":
        data_reader.read_users(data_path)  # data path paramter
        data_reader.read_reviews(data_path)  # data path paramter

        users = data_reader.dataset_of_users
        for user in users:
            repo.add_user(user)

        reviews = data_reader.dataset_of_reviews
        for review in reviews:
            repo.add_review(review)
            review._poster.add_review(review)
            review._podcast.add_review(review)