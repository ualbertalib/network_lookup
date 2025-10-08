from network_lookup.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_fqdn_localhost():
    # Act: perform the request
    response = client.get("/fqdn/localhost")

    # Assert: check that it succeeded
    assert response.status_code == 200

    data = response.json()

    # Basic sanity checks
    assert data["hostname"] == "localhost"
    assert data["addr"] == "127.0.0.1"

    # Optional: verify presence of other keys (don’t need to hardcode values)
    for key in ["id", "netmask", "gateway", "VMWareVLAN"]:
        assert key in data
