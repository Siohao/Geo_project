import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from geo_project.services.map_services import OverPass
from geo_project.models.map_models import OSMPointsResponse

@pytest.mark.parametrize(
    "if_result", (True, False)
)
@patch("geo_project.services.map_services.PlacesRepository")
@patch("geo_project.services.map_services.get_conn")
@patch("geo_project.services.map_services.release_conn")
def test_get_hiking_routes_summary(
                                mock_release_conn,
                                mock_get_conn,
                                mock_repo,
                                if_result,
                            ):
    
    mock_conn: Mock = Mock()
    mock_get_conn.return_value = mock_conn
    mock_release_conn.return_value = None

    mock_repo_instance: Mock = Mock()
    mock_repo.return_value = mock_repo_instance

    mock_client: Mock = Mock()
    mock_service:OverPass = OverPass(client=mock_client)

    mock_repo_instance.check_trails_for_point_in_db.return_value = if_result
    mock_client.get_hiking_routes.return_value = {"routes": ["r1"]}

    mock_repo_instance.read_trails.return_value = {"routes": "db"}

    result: Dict[str, Any] = mock_service.get_hiking_routes_summary(
        10, 10.0, 20.0, "ele", {}, 1
    )

    if if_result:
        mock_client.get_hiking_routes.assert_called_once()
        mock_repo_instance.save_trails.assert_called_once()
        mock_repo_instance.update_last_check_for_point.assert_called_once()
    else:
        mock_client.get_hiking_routes.assert_not_called()
        mock_repo_instance.save_trails.assert_not_called()
        mock_repo_instance.update_last_check_for_point.assert_not_called()

    mock_repo_instance.check_trails_for_point_in_db.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_repo_instance.read_trails.assert_called_once()
    mock_release_conn.assert_called_once_with(mock_conn)

    assert result == {"routes": "db"}

@patch("geo_project.services.map_services.OSMPointsResponse.parse_osm_points")
@patch("geo_project.services.map_services.PlacesRepository")
@patch("geo_project.services.map_services.get_conn")
@patch("geo_project.services.map_services.release_conn")
def test_get_viewpoints_summary(mock_release_conn, mock_get_conn, mock_repo, mock_parse):
    mock_conn: Mock = Mock()
    mock_get_conn.return_value = mock_conn
    mock_release_conn.return_value = None

    mock_repo_instance: Mock = Mock()
    mock_repo.return_value = mock_repo_instance

    mock_client: Mock = Mock()
    mock_service: OverPass = OverPass(client=mock_client)

    mock_client.get_viewpoints.return_value = {"viewpoints": {"view"}}
    mock_parse.return_value = {"parsed": "points"}

    result: OSMPointsResponse = mock_service.get_viewpoints_summary(
        10.0, 20.0, 10.0, 20.0, {}
    )

    mock_client.get_viewpoints.assert_called_once()
    mock_parse.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_repo_instance.save_many_points.assert_called_once_with(mock_conn, {"parsed": "points"})
    mock_release_conn.assert_called_once_with(mock_conn)

    assert result == {"parsed": "points"}
