import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Review


# Note: When using, make sure to run both and to run read_podcasts first BEFORE read_episodes
class CSVDataReader:
    def __init__(self):
        self.dataset_of_podcasts = []
        self.dataset_of_episodes = []
        self.dataset_of_authors = []
        self.dataset_of_categories = []
        self.dataset_of_users = []
        self.dataset_of_reviews = []

    def read_podcasts(self, data_path): #make it take data_path parameter
        #current_dir_name = os.path.dirname(os.path.abspath(__file__))
        #dir_name = os.path.dirname(os.path.abspath(current_dir_name))
        #podcast_file_name = os.path.join(dir_name, "data/podcasts.csv")
        podcast_file_name = os.path.join(data_path, "podcasts.csv")
        with open(podcast_file_name, encoding='utf-8', mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                podcast_id = int(row['id'].strip())
                title = row['title'].strip()
                img = row['image'].strip()
                desc = row['description'].strip()
                lang = row['language'].strip()
                website = row['website'].strip()
                itunes_id = int(row['itunes_id'].strip())
                author = row['author'].strip()
                categories = row['categories'].split('|')

                if author == "": #is
                    author = "Unknown Author"

                if author not in self.dataset_of_authors:
                    new_author = Author(len(self.dataset_of_authors) + 1, author)
                    self.dataset_of_authors.append(new_author)

                podcast = Podcast(podcast_id, new_author, title, img, desc, website, itunes_id, lang)
                new_author.add_podcast(podcast)

                for category in categories:
                    category = category.strip()
                    added = False

                    for existing in self.dataset_of_categories:
                        if existing.name == category:
                            podcast.add_category(existing)
                            added = True

                    if not added:
                        new_cat = Category(len(self.dataset_of_categories) + 1, category)
                        self.dataset_of_categories.append(new_cat)
                        podcast.add_category(new_cat)

                self.dataset_of_podcasts.append(podcast)

    def read_episodes(self, data_path): #make it take data_path parameter
        #current_dir_name = os.path.dirname(os.path.abspath(__file__))
        #dir_name = os.path.dirname(os.path.abspath(current_dir_name))
        #episode_file_name = os.path.join(dir_name, "data/episodes.csv")
        episode_file_name = os.path.join(data_path, "episodes.csv")
        with open(episode_file_name, encoding='utf-8', mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                episode_id = int(row['id'].strip())
                podcast_id = int(row['podcast_id'].strip())
                current_podcast = next((podcast for podcast in self.dataset_of_podcasts if podcast.id == podcast_id), None)
                title = row['title'].strip()
                audio= row['audio'].strip()
                if audio == "":         # Resolving issue with some episode links being empty
                    audio = "Link Not Available"
                audio_length = int(row['audio_length'].strip())
                desc = row['description'].strip()
                pub_date = row['pub_date'].strip()

                episode = Episode(episode_id, current_podcast, audio, audio_length, title, desc, pub_date)
                current_podcast.add_episode(episode)
                self.dataset_of_episodes.append(episode)


    def read_users(self, data_path):
        user_file_name = os.path.join(data_path, "users.csv")
        with open(user_file_name, encoding='utf-8', mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                user_id = int(row['id'].strip())
                username = row['username'].strip()
                password = row['password'].strip()

                user = User(user_id, username, password)
                self.dataset_of_users.append(user)

    def read_reviews(self, data_path):
        review_file_name = os.path.join(data_path, "reviews.csv")
        with open(review_file_name, encoding='utf-8', mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                user_id = int(row['user-id'].strip())
                podcast_id = int(row['podcast-id'].strip())
                rating = int(row['rating'].strip())
                comment = row['comment-text'].strip()

                podcast = next((podcast for podcast in self.dataset_of_podcasts if podcast.id == podcast_id),None)
                user = next((user for user in self.dataset_of_users if user.id == user_id),
                                       None)

                review = Review(user,podcast,rating,comment)
                user.add_review(review)
                podcast.add_review(review)
                self.dataset_of_reviews.append(review)




