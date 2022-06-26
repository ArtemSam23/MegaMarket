from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

items_json = {
    "items": [
        {
            "type": "CATEGORY",
            "name": "Root",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "parentId": None
        },
        {
            "type": "OFFER",
            "name": "Child1",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 100
        },
        {
            "type": "OFFER",
            "name": "Child2",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 200
        }
    ],
    "updateDate": "2022-02-01T12:00:00.000Z"
}

sales_json = {
    "items": [
        {
            "type": "OFFER",
            "name": "Child1",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 100
        },
        {
            "type": "OFFER",
            "name": "Child3",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 299
        }
    ],
    "updateDate": "2022-02-01T13:00:00.000Z"
}


def test_create_and_delete_items_simple():
    """Simple test fot creating items"""
    response = client.post(
        "/imports",
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Root",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }
    )
    assert response.status_code == 200

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200
    assert response.json() == {
        "type": "CATEGORY",
        "name": "Root",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": None,
        "parentId": None,
        "date": "2022-02-01T12:00:00.000Z",
        "children": []
    }

    response = client.delete(
        "/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200


def test_delete_non_existing_node():
    response = client.delete(
        "/delete/does-not-exist"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}


def test_get_non_existing_node():
    response = client.get(
        "/nodes/does-not-exist"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}


def test_create_items_non_existing_parent():
    response = client.post(
        "/imports",
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Root",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": "does-not-exist"
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'code': 400, 'message': 'Validation Failed'}

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}

    response = client.delete(
        "/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}


def test_create_items_with_parent():
    response = client.post(
        "/imports",
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Root",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                },
                {
                    "type": "CATEGORY",
                    "name": "Child",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }
    )
    assert response.status_code == 200

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200
    assert response.json() == {
        "type": "CATEGORY",
        "name": "Root",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": None,
        "parentId": None,
        "date": "2022-02-01T12:00:00.000Z",
        "children": [
            {
                "type": "CATEGORY",
                "name": "Child",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "price": None,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "date": "2022-02-01T12:00:00.000Z",
                "children": []
            }
        ]
    }

    response = client.delete(
        "/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200


def test_create_items_with_parent_and_price():
    response = client.post(
        "/imports",
        json=items_json
    )
    assert response.status_code == 200

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )

    assert response.status_code == 200
    assert response.json() == {
        "type": "CATEGORY",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "name": "Root",
        "price": 150,
        "parentId": None,
        "date": "2022-02-01T12:00:00.000Z",
        "children": [
            {
                "type": "OFFER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "name": "Child1",
                "price": 100,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "date": "2022-02-01T12:00:00.000Z",
                "children": None
            },
            {
                "type": "OFFER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
                "name": "Child2",
                "price": 200,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "date": "2022-02-01T12:00:00.000Z",
                "children": None
            }
        ]
    }

    response = client.delete(
        "/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
    )
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Item not found'}


def test_update_date():
    response = client.post(
        "/imports",
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Root",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                },
                {
                    "type": "CATEGORY",
                    "name": "Child",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }
    )
    assert response.status_code == 200

    response = client.post(
        "/imports",
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Child",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                }
            ],
            "updateDate": "2022-02-01T13:00:00.000Z"
        }
    )
    assert response.status_code == 200

    response = client.get(
        "/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200
    assert response.json() == {
        "type": "CATEGORY",
        "name": "Root",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": None,
        "parentId": None,
        "date": "2022-02-01T13:00:00.000Z",
        "children": [
            {
                "type": "CATEGORY",
                "name": "Child",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "price": None,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "date": "2022-02-01T13:00:00.000Z",
                "children": []
            }
        ]
    }

    response = client.delete(
        "/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    )
    assert response.status_code == 200


def test_sales():
    response = client.post(
        "/imports",
        json=items_json
    )
    assert response.status_code == 200

    response = client.post(
        "/imports",
        json=sales_json
    )
    assert response.status_code == 200

    response = client.get(
        "/sales",
        params={
            "date": "2022-02-20T11:00:00.000Z"
        }
    )
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        "/sales",
        params={
            "date": "2022-02-01T13:00:00.000Z"
        }
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type": "OFFER",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            "name": "Child2",
            "price": 200,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-01T12:00:00.000Z",
            "children": None
        },
        {
            "type": "OFFER",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            "name": "Child1",
            "price": 100,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-01T13:00:00.000Z",
            "children": None
        },
        {
            "type": "OFFER",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
            "name": "Child3",
            "price": 299,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-01T13:00:00.000Z",
            "children": None
        }
    ]

    response = client.get(
        "/sales",
        params={
            "date": "2022-02-01T12:00:00.000Z"
        }
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type": "OFFER",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            "name": "Child2",
            "price": 200,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-01T12:00:00.000Z",
            "children": None
        }
    ]
    assert client.delete("/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1").status_code == 200
