from unittest.mock import MagicMock, patch
import requests
from app.checker import check_site


@patch("app.checker.requests.get")
def test_site_up(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    result = check_site("https://example.com")
    assert result["is_up"] is True
    assert result["status_code"] == 200


@patch("app.checker.requests.get")
def test_site_down_on_500(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    result = check_site("https://example.com")
    assert check_site("https://example.com")["is_up"] is False


@patch("app.checker.requests.get", side_effect=requests.ConnectionError)
def test_site_down_on_exception(_):
    result = check_site("https://example.com")
    assert result["is_up"] is False
    assert result["status_code"] is None
