from typing import Optional, List

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

from pamps.security import HashedPassword
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pamps.models.post import Post
    from pamps.models.social import Social
    from pamps.models.like import Like


class User(SQLModel, table=True):
    """Represents the User Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: HashedPassword

    # it populates the .user attribute on the Content Model
    posts: List["Post"] = Relationship(back_populates="user")
    likes: List["Like"] = Relationship(back_populates="user")
    social_followers: List["Social"] = Relationship(back_populates="followers",  # Seguidores?
                                                    sa_relationship_kwargs={"foreign_keys": "[Social.to_id]"})
    social_following: List["Social"] = Relationship(back_populates="following",  # Seguindo?
                                                    sa_relationship_kwargs={"foreign_keys": "[Social.from_id]"})


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
