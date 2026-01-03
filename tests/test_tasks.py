import pytest
from ..tasks.schemas import TaskStatusEnum

@pytest.mark.parametrize(
    "headers_fixture, expected_status",
    [
        ("admin_headers", 201),
        ("koord_headers", 201),
        ("monter_headers", 403),
    ]
)

def test_create_task_permissions(client, request, headers_fixture, expected_status):
    headers = request.getfixturevalue(headers_fixture)

    response = client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": "Test task",
            "description": "Opis",
            "address": "Katowice",
            "execution_date": None
        }
    )

    assert response.status_code == expected_status

    if expected_status == 201:
        assert response.json()["title"] == "Test task"

#------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "headers_fixture",
    ["admin_headers", "koord_headers", "monter_headers"]
)
def test_endpoint_accessible_for_all_users(client, request, headers_fixture):
    headers = request.getfixturevalue(headers_fixture)

    response = client.get("/tasks/unassigned", headers=headers)

    assert response.status_code == 200

#------------------------------------------------------------------------------------------

def test_endpoint_requires_auth(client):
    response = client.get("/tasks/unassigned")
    assert response.status_code == 401

#------------------------------------------------------------------------------------------

def test_my_tasks_returns_only_user_tasks(client,admin_headers,monter_headers):
    admin = admin_headers
    task = client.post(
        "/tasks/",
        headers=admin,
        json={
            "title": "Admin task",
            "description": "Opis",
            "address": "x",
            "execution_date": None
        }
    ).json()

    client.post(f"/tasks/assign/{task['id']}?user_to_assign_id=3", headers=admin)

    response = client.get("/tasks/my-tasks", headers=monter_headers)
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Admin task" 

def test_get_task_by_id(client,admin_headers,koord_headers,monter_headers):
    admin = admin_headers
    task = client.post(
        "/tasks/",
        headers=admin,
        json={
            "title": "Admin task",
            "description": "Opis",
            "address": "x",
            "execution_date": None
        }
    ).json()

    task_id = task["id"]

    response_admin = client.get(f"/tasks/{task_id}", headers=admin_headers)
    assert response_admin.status_code == 200
    assert response_admin.json()["id"] == task_id

    response_koord = client.get(f"/tasks/{task_id}", headers=koord_headers)
    assert response_koord.status_code == 200
    assert response_koord.json()["id"] == task_id

    response_monter = client.get(f"/tasks/{task_id}", headers=monter_headers)
    assert response_monter.status_code == 200
    assert response_monter.json()["id"] == task_id

def test_update_task_endpoint(client, admin_headers, koord_headers, monter_headers):
    admin = admin_headers
    task = client.post(
        "/tasks/",
        headers=admin,
        json={
            "title": "Admin task",
            "description": "Opis",
            "address": "x",
            "execution_date": None
        }
    ).json()

    task_id = task["id"]

    updated_task = {
        "title": "Admin task",
        "description": "nowy opis",
        "address": "nowa lokalizacja",
        "execution_date": None
    }

    response_admin = client.put(
        f"/tasks/{task_id}",
        headers=admin_headers,
        json=updated_task
    )

    assert response_admin.status_code == 200
    data = response_admin.json()
    assert data["description"] == "nowy opis"
    assert data["address"] == "nowa lokalizacja"

    response_koord = client.put(
        f"/tasks/{task_id}",
        headers=koord_headers,
        json=updated_task
    )

    assert response_koord.status_code == 200
    data = response_koord.json()
    assert data["description"] == "nowy opis"
    assert data["address"] == "nowa lokalizacja"

    response_monter = client.put(
        f"/tasks/{task_id}",
        headers=monter_headers,
        json=updated_task
    )

    assert response_monter.status_code == 200
    data = response_monter.json()
    assert data["description"] == "nowy opis"
    assert data["address"] == "nowa lokalizacja"



def test_assign_task_endpoint(client,admin_headers,koord_headers,monter_headers):
    task = client.post("/tasks/",
                       headers=admin_headers,
                       json={
                           "title": "Admin task",
                            "description": "Opis",
                            "address": "x",
                            "execution_date": None
                       }).json()
    
    task_id = task["id"]

    user_id_to_assign = 3

    response_admin = client.post(
        f"/tasks/assign/{task_id}?user_to_assign_id={user_id_to_assign}",
        headers=admin_headers
    )

    assert response_admin.status_code == 200
    data = response_admin.json()
    assert data["assigned_user_id"] == user_id_to_assign

    response_repeat = client.post(
        f"/tasks/assign/{task_id}?user_to_assign_id={user_id_to_assign}",
        headers=admin_headers
    )
    assert response_repeat.status_code == 400

    task2 = client.post("/tasks/",
                       headers=admin_headers,
                       json={
                           "title": "Admin task 2",
                            "description": "Opis",
                            "address": "x",
                            "execution_date": None
                       }).json()
    
    task2_id = task2["id"]

    response_koord = client.post(
        f"/tasks/assign/{task2_id}?user_to_assign_id={user_id_to_assign}",
        headers=koord_headers
    )
    assert response_koord.status_code == 200
    data = response_koord.json()
    assert data["assigned_user_id"] == user_id_to_assign

    task3 = client.post("/tasks/",
                       headers=admin_headers,
                       json={
                           "title": "Admin task 3",
                            "description": "Opis",
                            "address": "x",
                            "execution_date": None
                       }).json()
    
    task3_id = task3["id"]

    response_monter = client.post(
        f"/tasks/assign/{task3_id}?user_to_assign_id={user_id_to_assign}",
        headers=monter_headers
    )
    assert response_monter.status_code == 200
    data = response_monter.json()
    assert data["assigned_user_id"] == user_id_to_assign

#--------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "headers_fixture, new_status, expected_status_code",
    [
        ("admin_headers", TaskStatusEnum.IN_PROGRESS.value, 200),
        ("koord_headers", TaskStatusEnum.DONE.value, 200),
        ("monter_headers", TaskStatusEnum.REJECTED.value, 200),
    ]
)

def test_change_status_endpoint(client, request, headers_fixture, new_status, expected_status_code):
    headers = request.getfixturevalue(headers_fixture)

    task = client.post("/tasks/",
                       headers=request.getfixturevalue("admin_headers"),
                       json={
                           "title": "Admin task",
                            "description": "Opis",
                            "address": "x",
                            "execution_date": None
                       }).json()
    
    task_id = task["id"]

    response = client.put(
        f"/tasks/status/{task_id}",
        headers=headers,
        json={"status": new_status}
    )

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        data = response.json()
        assert data["status"] == new_status
        assert data["id"] == task_id


def test_delete_task_endpoint(client, admin_headers):
    task = client.post("/tasks/",
                       headers=admin_headers,
                       json={
                           "title": "Admin task",
                            "description": "Opis",
                            "address": "x",
                            "execution_date": None
                       }).json()
    
    task_id = task["id"]

    admin_response = client.delete(
        f"/tasks/delete/{task_id}",
        headers=admin_headers
    )

    assert admin_response.status_code == 200
    data = admin_response.json()
    assert data["detail"] == "Task deleted"

    get_response = client.get(
        f'/tasks/{task_id}',
        headers=admin_headers
    )
    assert get_response.status_code == 404