from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from pamps.auth import AuthenticatedUser
from pamps.db import ActiveSession
from pamps.models import Social
from pamps.models.post import Post
from pamps.models.social import SocialResponse, TimelineResponse
from pamps.models.user import User, UserRequest, UserResponse

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""

    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(*, session: Session = ActiveSession, username: str):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    db_user = User.model_validate(user)  # transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/follow/{user_id}", response_model=SocialResponse, status_code=status.HTTP_201_CREATED)
def follow(*, user_id: int, session: Session = ActiveSession, user: User = AuthenticatedUser):
    """Follow user"""
    if user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot follow yourself")

    user_to_follow = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    if not user_to_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    social = session.exec(
        select(Social).where(Social.from_id == user.id).where(Social.to_id == user_id)
    ).first()
    if social:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You already follow this user")

    db_social = Social(from_id=user.id, to_id=user_id)
    session.add(db_social)
    session.commit()
    session.refresh(db_social)
    return db_social


@router.get("/timeline", response_model=List[TimelineResponse])
async def timeline(*, session: Session = ActiveSession, user: User = AuthenticatedUser):
    """Timeline from authenticated user"""
    following_ids = session.exec(
        select(Social.to_id).where(Social.from_id == user.id)
    ).all()

    posts = session.exec(
        select(Post).where(Post.user_id.in_(following_ids)).order_by(Post.date.desc())
    ).all()
    return posts
