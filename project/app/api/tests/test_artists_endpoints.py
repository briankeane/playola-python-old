def test_artists_empty_array(test_app_with_db):
    response = test_app_with_db.get("/v1/artists")
    assert response.status_code == 200
    assert response.json() == []
