from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from pamps.models.user import User


class Social(SQLModel, table=True):
    """Represents the Social model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    from_id: Optional[int] = Field(foreign_key="user.id", nullable=False)  # Usuário logado
    to_id: Optional[int] = Field(foreign_key="user.id", nullable=False)  # Usuário a ser seguido
    date: datetime = Field(default=datetime.now(timezone.utc), nullable=False)

    followers: Optional["User"] = Relationship(
        back_populates="social_followers", sa_relationship_kwargs={"primaryjoin": "Social.to_id == User.id",
                                                                   "overlaps": "social_followers,following"}
    )
    following: Optional["User"] = Relationship(
        back_populates="social_following", sa_relationship_kwargs={"primaryjoin": "Social.from_id == User.id",
                                                                   "overlaps": "social_following"}
    )


class SocialResponse(BaseModel):
    """Serializer for Social Response"""

    id: int
    from_id: int
    to_id: int
    date: datetime


class TimelineResponse(BaseModel):
    """Serializer for Timeline Response"""

    user_id: int
    text: str
    date: datetime
