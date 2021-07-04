from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
  from .twitter_account import TwitterAccount
  from .hashtag import Hashtag
  from .hashtag_collection import HashtagCollection
  from .location import Location


class User(Base):
  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean(), default=True)
  is_superuser = Column(Boolean(), default=False)
