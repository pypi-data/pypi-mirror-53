from typing import Any

from zpov.pages import Pages

# FIXME
TestClient = Any


def test_home(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    response = client.get("/")
    assert response.status_code == 302
    redirect_url = response.headers["location"]
    response = client.get(redirect_url)
    assert response.status_code == 200


def test_view_index(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    response = client.get("/view/index")
    assert response.status_code == 200


def test_edit_form(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    response = client.get("/edit/index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert "textarea" in html


def test_save_page(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    response = client.post(
        "/save/index", data={"text": "# Welcome\nThis has been added"}
    )
    response = client.get("/view/index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "This has been added" in html


def test_add_form(client: TestClient, pages: Pages) -> None:
    response = client.get("/add?name=index")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert 'action="/add"' in html


def test_add_page(client: TestClient, pages: Pages) -> None:
    response = client.post("/add", data={"name": "index", "title": "Welcome"})
    assert response.status_code == 302
    redirect_url = response.headers["location"]
    response = client.get(redirect_url)
    assert response.status_code == 200


def test_view_in_subdir(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    pages.save("one/foo", "# Foo\n")
    response = client.get("/view/one/foo")
    assert response.status_code == 200


def test_search(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    pages.save("foo/bar", "# Bar\nMentions foo")
    pages.save("foo/baz", "# Baz\nAlso mentions foo")
    response = client.get("/search")
    assert response.status_code == 200
    html = response.data.decode()
    assert "form" in html
    assert 'action="/search"' in html

    response = client.get("/search?pattern=foo")
    assert response.status_code == 200
    html = response.data.decode()
    assert 'href="/view/foo/bar"' in html, html


def test_add_conflict(client: TestClient, pages: Pages) -> None:
    pages.save("index", "# Welcome\n")
    response = client.post("/add", data={"name": "index", "title": "Welcome"})
    assert response.status_code == 409
