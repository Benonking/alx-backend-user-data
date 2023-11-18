#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Add a new user to the database.

        Args:
            email (str): User's email.
            hashed_password (str): Hashed password for the user.

        Returns:
            User: The created User object.
        """
        try:
            added_user = User(email=email, hashed_password=hashed_password)
            # add user to a session
            self._session.add(added_user)
            # save to db
            self._session.commit()
        except Exception:
            self._session.rollback()
            added_user = None
        return added_user

    def find_user_by(self, **kwargs: dict) -> Union[User, None]:
        """Find a user in the database based on the input arguments.
        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first User object matching the query.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If an invalid query argument is provided.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """update a user in the database
            based on user_id and the input arguments.

        Args:
            user_id : user id
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first User object matching the query.

        Raises:
            ValueError: If argument does not corespond to a useratrribute.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
