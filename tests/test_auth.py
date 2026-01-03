def test_register_user(client):
    response = client.post("/auth/register",
        json={
            "username": "admin",
            "password": "admin123",
            "user_role": 1
        })
    
    assert response.status_code == 201
    assert response.json()["username"] == "admin"

def test_login_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body