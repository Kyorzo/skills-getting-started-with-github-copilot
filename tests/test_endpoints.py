import pytest


def test_root_redirect(client):
    # prevent following redirects so we can assert the redirect response
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (302, 307)
    assert "/static/index.html" in resp.headers["location"]


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success_and_persistence(client):
    email = "testuser1@mergington.edu"
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json()["message"]

    data = client.get("/activities").json()
    assert email in data["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    email = "testdup@mergington.edu"
    # First signup
    r1 = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert r1.status_code == 200
    # Duplicate signup
    r2 = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert r2.status_code == 400
    assert r2.json().get("detail") == "Student already signed up"


def test_signup_invalid_activity_returns_404(client):
    r = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert r.status_code == 404


def test_unregister_success_and_persistence(client):
    email = "michael@mergington.edu"
    # Ensure michael exists initially
    before = client.get("/activities").json()
    assert email in before["Chess Club"]["participants"]

    r = client.post("/activities/Chess%20Club/unregister", params={"email": email})
    assert r.status_code == 200
    assert f"Unregistered {email}" in r.json()["message"]

    after = client.get("/activities").json()
    assert email not in after["Chess Club"]["participants"]


def test_unregister_not_registered_returns_400(client):
    email = "notregistered@mergington.edu"
    r = client.post("/activities/Chess%20Club/unregister", params={"email": email})
    assert r.status_code == 400
    assert r.json().get("detail") == "Student is not registered for this activity"


def test_unregister_invalid_activity_returns_404(client):
    r = client.post("/activities/Nope/unregister", params={"email": "a@b.com"})
    assert r.status_code == 404
