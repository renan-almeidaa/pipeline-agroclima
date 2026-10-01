import pytest
import requests

from src.ingestion.ibge import _erro_transitorio


def _http_error(status: int) -> requests.HTTPError:
    """Cria um HTTPError com o status code informado."""
    resp = requests.Response()
    resp.status_code = status
    return requests.HTTPError(response=resp)


@pytest.mark.parametrize(
    "exc, esperado",
    [
        # TODO: Timeout -> True
        (requests.exceptions.Timeout(), True), 
        # TODO: ConnectionError -> True
        (requests.exceptions.ConnectionError(), True),
        # TODO: 503 e 429 -> True
        (_http_error(503), True),
        (_http_error(429), True),
        # TODO: 404 e 400 -> False
        (_http_error(404), False),
        (_http_error(400), False),
        # TODO: ValueError -> False
        (ValueError(), False),
        # TODO: HTTPError sem response -> ?
        (requests.HTTPError(), False)
    ],
)
def test_erro_transitorio(exc, esperado):
    assert _erro_transitorio(exc) == esperado