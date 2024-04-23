#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to Db
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """filter user by email
        """
        filltred = ({key: value for key, value in kwargs.items()
                     if hasattr(User, key)})
        if not filltred:
            raise InvalidRequestError()
        user = self._session.query(User).filter_by(**filltred).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user by id
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        to_update = ({key: value for key, value in kwargs.items()
                     if hasattr(User, key)})
        if not to_update:
            raise ValueError()
        for key, value in to_update.items():
            setattr(user, key, value)
        self._session.commit()
