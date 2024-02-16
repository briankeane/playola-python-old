def test_curators_empty_array(test_app_with_db):
    response = test_app_with_db.get("/v1/curators")
    assert response.status_code == 200
    assert response.json() == []
