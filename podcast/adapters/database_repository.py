from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session

from podcast.domainmodel.model import User, Podcast, Episode, Review, Playlist, Author, Category
from podcast.adapters.repository import AbstractRepository, RepositoryException

repo_instance = None

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one() #_username
        except NoResultFound:
            pass

        return user

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def remove_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.delete(podcast)
            scm.commit()

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.merge(author)
            scm.session.merge(author)
            scm.commit()

    def add_category(self, cat: Category):
        with self._session_cm as scm:
            scm.session.merge(cat)
            scm.commit()

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def remove_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.delete(episode)
            scm.commit()

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            podcast = self._session_cm.session.query(Podcast).filter_by(_id=podcast_id).one()
        except NoResultFound:
            pass
        return podcast

    def get_reviews(self):
        return self._session_cm.session.query(Review).all()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def add_to_user_playlist(self, user: User, item: Podcast | Episode):
        with self._session_cm as scm:
            playlist = user._playlist
            if isinstance(item, Podcast):
                playlist._podcast_list.append(item)
            else:
                playlist._episode_list.append(item)
            scm.session.merge(playlist)
            scm.commit()

    def remove_from_user_playlist(self, user: User, item: Podcast | Episode):
        with self._session_cm as scm:
            playlist = user._playlist
            if isinstance(item, Podcast):
                playlist._podcast_list.remove(item)
            else:
                playlist._episode_list.remove(item)
            scm.session.merge(playlist)
            scm.commit()

    def get_user_playlist(self, user: User):
        return user.playlist

    def get_episode(self, podcast_id, episode_id):
        return self._session_cm.session.query(Episode).filter_by(_id=episode_id).one()

    def get_episodes(self, podcast: Podcast):
        return self._session_cm.session.query(Episode).filter_by(podcast=podcast).all()

    def get_number_of_episodes(self, podcast: Podcast):
        return self._session_cm.session.query(Episode).filter_by(podcast=podcast).count()

    def get_number_of_podcasts(self):
        with self._session_cm as scm:
            return scm.session.query(Podcast).count()

    def get_playlist_total(self, user: User):
        playlist = user._playlist
        total_podcasts = len(playlist._podcast_list)
        total_episodes = len(playlist._podcast_list)
        return total_podcasts + total_episodes

    def get_podcasts(self):
        return self._session_cm.session.query(Podcast).all()

    def get_user_episode_playlist(self, user: User):
        return user._playlist._episode_list

    def get_user_podcast_playlist(self, user: User):
        return user._playlist._podcast_list

    def search_podcasts(self, search_term: str, search_filter: str):
        results = []

        if search_term != "":
            if search_filter == "Title":
                results = self._session_cm.session.query(Podcast).filter(Podcast._title.ilike('%' + search_term + '%')).all()

            if search_filter == "Category":
                results = self._session_cm.session.query(Podcast).join(Podcast.categories).filter(Category._name.ilike('%' + search_term + '%')).all()

            if search_filter == "Author":
                results = self._session_cm.session.query(Podcast).join(Author).filter(Author._name.ilike('%' + search_term + '%')).all()

            if search_filter == "Language":
                results = self._session_cm.session.query(Podcast).filter(Podcast._language.ilike('%' + search_term + '%')).all()

        return results

    def get_user_count(self):
        users = self._session_cm.session.query(User).all()
        if users is None:
            return 0
        return len(users)
