from app.main import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health_returns_ok():
    res = client().get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_index_returns_message():
    res = client().get("/")
    assert res.status_code == 200
    assert "Hello from the cloud microservice" in res.get_json()["message"]


def test_hello_uses_name():
    res = client().get("/hello/Asha")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Hello, Asha!"


def test_info_contains_hostname():
    res = client().get("/info")
    data = res.get_json()
    assert res.status_code == 200
    assert "hostname" in data and data["hostname"]


def test_add_endpoint():
    res = client().get("/add/2/3")
    assert res.status_code == 200
    assert res.get_json()["result"] == 5


def test_unknown_route_returns_404():
    assert client().get("/does-not-exist").status_code == 404
