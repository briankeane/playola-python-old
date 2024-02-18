from app import main


def test_ping(test_app):
    response = test_app.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {
        "environment": "dev",
        "responds": True,
        "testing": True,
        "base_url": "http://localhost:8004",
        "client_base_url": "http://localhost:3000",
    }
