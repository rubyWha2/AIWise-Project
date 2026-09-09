from backend.src import routes
from tests.test_helpers import FakeConnection, FakeCursor


ARTICLES = [
    (
        1,
        "What Is Data Handling in Business?",
        "<p>Data handling is the process of collecting, storing, analysing, processing, and presenting information securely and accurately.</p>",
        "Data Protection",
    ),
    (
        2,
        "The Data Lifecycle",
        "<p>The data lifecycle is the sequence of stages that data goes through from its initial creation or collection to its secure and compliant destruction.</p>",
        "Data Protection",
    ),
]


def test_get_articles_returns_database_articles(client, monkeypatch):
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(FakeCursor(fetchall=ARTICLES)))

    response = client.get("/api/articles")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "article_id": 1,
            "title": "What Is Data Handling in Business?",
            "content": "<p>Data handling is the process of collecting, storing, analysing, processing, and presenting information securely and accurately.</p>",
            "category": "Data Protection",
        },
        {
            "article_id": 2,
            "title": "The Data Lifecycle",
            "content": "<p>The data lifecycle is the sequence of stages that data goes through from its initial creation or collection to its secure and compliant destruction.</p>",
            "category": "Data Protection",
        },
    ]


def test_get_inv_article_returns_one_article(client, monkeypatch):
    cursor = FakeCursor(fetchone=[ARTICLES[0]])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/articles/1")

    assert response.status_code == 200
    assert response.get_json()["article_id"] == 1
    assert response.get_json()["title"] == "What Is Data Handling in Business?"


def test_get_inv_article_returns_404_when_missing(client, monkeypatch):
    cursor = FakeCursor(fetchone=[None])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/articles/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Article not found"
