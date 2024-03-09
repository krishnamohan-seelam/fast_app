from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from fast_app.main import app, get_db
from fast_app.db.item import Base, DBItem

client = TestClient(app)
DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSession()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)
    test_item = DBItem(
        id=100, name="Master Test Item", description="created master test item"
    )
    test_session = TestingSession()
    test_session.add(test_item)
    test_session.commit()
    test_session.close()


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=test_engine)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "application working"


def test_create_item():
    response = client.post(
        "/items",
        json={"name": "test item", "description": "test item created"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test item"
    assert data["description"] == "test item created"
    assert "id" in data


def test_read_item():
    item_id = 100
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Master Test Item"
    assert data["description"] == "created master test item"
    assert "id" in data


def test_update_item():
    item_id = 100
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Master Test Item", "description": "updated master test item"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Master Test Item"
    assert data["description"] == "updated master test item"
    assert "id" in data


def test_delete_item():
    item_id = 100
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Master Test Item"
    assert "id" in data
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404, response.text
