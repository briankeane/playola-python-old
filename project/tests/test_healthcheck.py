from app import main


def test_ping(test_app):
    response = test_app.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "responds": True, "testing": True}