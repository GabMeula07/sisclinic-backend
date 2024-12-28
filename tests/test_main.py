from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste1@gmail.com",
            "password": "31324664",
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["id"] == 1
    assert response.json()["email"] == "teste1@gmail.com"


def test_create_user_return_err(client):
    response = client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste1@gmail.com",
            "password": "31324664",
        },
    )
    response2 = client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste1@gmail.com",
            "password": "31324664",
        },
    )
    print(response2.json())
    assert response2.status_code == HTTPStatus.BAD_REQUEST
    assert response2.json()["detail"] == "Email already exists"
