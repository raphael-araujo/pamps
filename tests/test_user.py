import pytest


@pytest.mark.order(3)
def test_follow_user(api_client_user1, api_client_user2):
    """User2 will follow user1"""

    api_client_user1.get(
        "/user/",
    )
    response = api_client_user2.post(
        "user/follow/1",
    )
    assert response.status_code == 201


@pytest.mark.order(3)
def test_follow_yourself_should_return_status_403(api_client_user1, api_client_user2):
    """User1 will try follow yourself."""

    response = api_client_user1.post(
        "user/follow/1",
    )

    assert response.status_code == 403
    assert "You cannot follow yourself" in response.json()["detail"]


@pytest.mark.order(3)
def test_timeline(api_client_user1, api_client_user2):
    """Timeline from user2"""

    response = api_client_user2.get(
        "user/timeline",
    )

    assert response.status_code == 200
    assert "hello test 1" in response.json()[0]["text"]
