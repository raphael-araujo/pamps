from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pamps.models.user import User
    from pamps.models.post import Post


class Like(SQLModel, table=True):
    """Represents the Like model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id", nullable=False)
    post_id: Optional[int] = Field(foreign_key="post.id", nullable=False)

    user: Optional["User"] = Relationship(back_populates="likes")
    post: Optional["Post"] = Relationship(back_populates="likes")
