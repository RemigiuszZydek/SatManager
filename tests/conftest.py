import  pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database.database import Base, get_db
from ..users.models import Role

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session",autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def seed_roles():
    db = TestingSessionLocal()
    roles = ["ADMIN","KOORDYNATOR","MONTER"]

    for role in roles:
        db.add(Role(name=role))

    db.commit()
    db.close()

@pytest.fixture()
def admin_headers(client):
    client.post("/auth/register",
        json={
            "username": "admin",
            "password": "admin123",
            "user_role": 1
        })
    
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture()
def koord_headers(client):
    client.post("/auth/register",
        json={
            "username": "koordynator",
            "password": "koordynator123",
            "user_role": 2
        })
    
    response = client.post(
        "/auth/login",
        data={
            "username": "koordynator",
            "password": "koordynator123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture()
def monter_headers(client):
    client.post("/auth/register",
        json={
            "username": "monter",
            "password": "monter123",
            "user_role": 3
        })
    
    response = client.post(
        "/auth/login",
        data={
            "username": "monter",
            "password": "monter123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }