"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

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

    def add_user(self, email, hashed_password):
        """Add a new user to the database.

        Args:
            email (str): User's email.
            hashed_password (str): Hashed password for the user.

        Returns:
            User: The created User object.
        """
        added_user = User(email=email, hashed_password=hashed_password)
        # add user to a session
        self._session.add(added_user)
        # save to db
        self._session.commit()
        return added_user

    def find_user_by(self, **kwargs):
        """Find a user in the database based on the input arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first User object matching the query.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If an invalid query argument is provided.
        """
        try:
            # query the db using provide key , value pair
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound('Not Found')
            return user
        except InvalidRequestError:
            for k in kwargs.keys():
                # check if atrribute exists
                if not hasattr(User, k):
                    raise InvalidRequestError('Invalid')

    def update_user(self, user_id, **kwargs):
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
        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                # check if atrribute exists
                if hasattr(User, k):
                    setattr(user, k, v)
                else:
                    raise ValueError(k + 'Not attribute of User object')
        except NoResultFound:
            raise NoResultFound('Not found')
