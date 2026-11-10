import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.helper.helpers import require_admin, require_author

def override_author_ws():
    return {"id": "AUTH001", "role": "author", "name": "Test Author"}

def override_admin_ws():
    return {"id": "ADMIN01", "role": "admin", "name": "Test Admin"}

@pytest.fixture
def client():
    app.dependency_overrides[require_author] = override_author_ws
    app.dependency_overrides[require_admin] = override_admin_ws
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def create_tkt(client):
    payload={
        "book_id": 'BK001',
        "subject": "Test",
        "description": "Testing....",
        "category": "Account Level"
    }

    response = client.post('/ticket/author/create', data=payload)

    assert response.status_code in (200, 201), response.text
    resp_data = response.json()

    ticket_code = resp_data.get('ticket_code') or resp_data.get('data', {}).get('ticket_code')

    assert ticket_code is not None, f"Could not get ticket code = {resp_data}"
    yield ticket_code


def test_websockets_connects_and_sends(client, create_tkt):
    ticket_code = create_tkt

    print("\n1. Opening author connection")

    with client.websocket_connect(
        f"/ticket/ws/author/chat?ticket_code={ticket_code}"
    ) as author_ws:

        print("2. Author connected")

        with client.websocket_connect(
            f"/ticket/ws/admin/chat?ticket_code={ticket_code}"
        ) as admin_ws:

            print("3. Admin connected")

            # Author sends a message
            print("4. Author sending message")

            author_ws.send_json({
                "message": "Hello admin"
            })

            print("5. Waiting for admin message")

            admin_data = admin_ws.receive_json()

            print("6. Admin received:", admin_data)

            assert admin_data["message"] == "Hello admin"
            assert admin_data["sender"] == "Test Author"

            author_own_broadcast = author_ws.receive_json()

            assert author_own_broadcast["message"] == "Hello admin"

            # Admin sends a message
            print("7. Admin sending message")

            admin_ws.send_json({
                "message": "Hello from Admin"
            })

            author_data = author_ws.receive_json()

            assert author_data["message"] == "Hello from Admin"
            assert author_data["sender"] == "Test Admin"

            admin_own_broadcast = admin_ws.receive_json()

            assert admin_own_broadcast["message"] == "Hello from Admin"

            print("8. Both messages successfully exchanged")