import pytest


@pytest.mark.order(1)
def test_post_create_user1(api_client_user1):
    """Create 2 posts with user 1"""
    for n in (1, 2):
        response = api_client_user1.post(
            "/post/",
            json={
                "text": f"hello test {n}",
            },
        )
        assert response.status_code == 201
        result = response.json()
        assert result["text"] == f"hello test {n}"
        assert result["parent_id"] is None


@pytest.mark.order(2)
def test_reply_on_post_1(api_client, api_client_user1, api_client_user2):
    """each user will add a reply to the first post"""
    posts = api_client.get("/post/user/user1/").json()
    first_post = posts[0]
    for n, client in enumerate((api_client_user1, api_client_user2), 1):
        response = client.post(
            "/post/",
            json={
                "text": f"reply from user{n}",
                "parent_id": first_post["id"],
            },
        )
        assert response.status_code == 201
        result = response.json()
        assert result["text"] == f"reply from user{n}"
        assert result["parent_id"] == first_post["id"]


@pytest.mark.order(3)
def test_post_list_without_replies(api_client):
    response = api_client.get("/post/")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for result in results:
        assert result["parent_id"] is None
        assert "hello test" in result["text"]


@pytest.mark.order(3)
def test_post1_detail(api_client):
    posts = api_client.get("/post/user/user1/").json()
    first_post = posts[0]
    first_post_id = first_post["id"]

    response = api_client.get(f"/post/{first_post_id}/")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == first_post_id
    assert result["user_id"] == first_post["user_id"]
    assert result["text"] == "hello test 1"
    assert result["parent_id"] is None
    replies = result["replies"]
    assert len(replies) == 2
    for reply in replies:
        assert reply["parent_id"] == first_post_id
        assert "reply from user" in reply["text"]


@pytest.mark.order(3)
def test_all_posts_from_user1(api_client):
    response = api_client.get("/post/user/user1/")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for result in results:
        assert result["parent_id"] is None
        assert "hello test" in result["text"]


@pytest.mark.order(3)
def test_all_posts_from_user1_with_replies(api_client):
    response = api_client.get("/post/user/user1/", params={"include_replies": True})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 3


@pytest.mark.order(3)
def test_like_route(api_client, api_client_user1):
    posts = api_client.get("/post/user/user1/").json()
    second_post = posts[1]["id"]

    response = api_client_user1.post(f"/post/{second_post}/like/")
    assert response.status_code == 201
    result = response.json()
    assert result["user_id"] == 1
    assert result["post_id"] == 2


@pytest.mark.order(3)
def test_like_route_with_non_existent_post_id(api_client_user1):
    response = api_client_user1.post("/post/0/like/")
    assert response.status_code == 404
    assert "Post not found" in response.json()["detail"]


@pytest.mark.order(4)
def test_like_route_with_post_already_liked(api_client, api_client_user1):
    response = api_client_user1.post(f"/post/2/like/")
    assert response.status_code == 400
    assert "Post already liked" in response.json()["detail"]


@pytest.mark.order(4)
def test_liked_posts_route(api_client):
    response = api_client.get("/post/likes/user1/")
    assert response.status_code == 200
    result = response.json()
    assert result[0]["id"] == 2
    assert result[0]["text"] == "hello test 2"
    assert result[0]["user_id"] == 1


@pytest.mark.order(4)
def test_liked_posts_route_with_non_existent_username(api_client):
    response = api_client.get("/post/likes/user000/")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
