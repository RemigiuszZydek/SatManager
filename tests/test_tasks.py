def test_create_task_as_admin(client,admin_headers):
    response = client.post(
        "/tasks/",
        headers=admin_headers,
        json={
            "title": "Test task",
            "description": "Opis",
            "address": "Katowice",
            "execution_date": None
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"

def test_create_task_as_koord(client,koord_headers):
    response = client.post(
        "/tasks/",
        headers=koord_headers,
        json={
            "title": "Test task",
            "description": "Opis",
            "address": "Katowice",
            "execution_date": None
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"

def test_create_task_as_monter(client,monter_headers):
    response = client.post(
        "/tasks/",
        headers=monter_headers,
        json={
            "title": "Test task",
            "description": "Opis",
            "address": "Katowice",
            "execution_date": None
        }
    )
    assert response.status_code == 403
    


    