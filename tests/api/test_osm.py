import pytest

@pytest.mark.parametrize("endpoint", ["/OSM/peaks", "/OSM/viewpoints"])

def test_bbox_endpoint(client, bbox_params, endpoint):
    response = client.get(endpoint, params=bbox_params)
    assert response.status_code == 200
    data = response.json()
    assert "features" in data

@pytest.mark.parametrize("endpoint", ["/OSM/routes", "/OSM/premade_routes"])

def test_coor_endpoint(client, location_params, endpoint):
    response = client.get(endpoint, params= location_params)
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data