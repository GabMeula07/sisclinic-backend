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
    client.post(
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


def test_create_access_token(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    assert token_response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_create_access_token_err_not_user(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste2@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    assert token_response.status_code == HTTPStatus.UNAUTHORIZED
    assert "detail" in data
    assert data["detail"] == "Invalid Email or Password"


def test_create_access_token_err_wrong_pass(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "3132466"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    assert token_response.status_code == HTTPStatus.UNAUTHORIZED
    assert "detail" in data
    assert data["detail"] == "Invalid Email or Password"


def test_auth_users_me(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/users/me", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == 1
    assert response.json()["email"] == "teste@gmail.com"


def test_create_profile(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == profile


def test_create_profile_err_exists(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    response = client.post("/users/profile", headers=headers, json=profile)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Profile already exists"


def test_get_profile(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    response = client.get("/users/profile", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == profile


def test_scheduler_rooms(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    room = {
        "room": "string",
        "date_scheduled": "2025-08-15",
        "time_scheduled": "string",
        "is_fixed": False,
    }
    response = client.post("/rooms", json=room, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert "scheduled" in response.json()
    assert response.json()["msg"] == "OK"
    assert response.json()["scheduled"][0] == room


def test_get_profile_err_not_found(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/users/profile", headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Profile User not Found"


def test_scheduler_room_err_user_not_active(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    room = {
        "room": "string",
        "date_scheduled": "2025-08-15",
        "time_scheduled": "string",
        "is_fixed": False,
    }
    response = client.post("/rooms", json=room, headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "User is not active"


def test_scheduler_already_exists(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    room = {
        "room": "string",
        "date_scheduled": "2025-08-15",
        "time_scheduled": "string",
        "is_fixed": False,
    }
    response = client.post("/rooms", json=room, headers=headers)
    response = client.post("/rooms", json=room, headers=headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Schedule already exists"


def test_get_scheduler_rooms(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}

    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    room = {
        "room": "string",
        "date_scheduled": "2025-08-15",
        "time_scheduled": "string",
        "is_fixed": False,
    }
    response = client.post("/rooms", json=room, headers=headers)
    response = client.get("/myrooms", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert "prox_index" in response.json()
    assert "scheduled" in response.json()
    assert response.json()["scheduled"][0] == {
        "id": 1,
        "user_id": 1,
        "room": "string",
        "date_scheduled": "2025-08-15",
        "time_scheduled": "string",
        "is_fixed": False,
    }


def test_fixed_scheduler_already_exists(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    room = {
        "room": "string",
        "date_scheduled": "2025-01-30",
        "time_scheduled": "string",
        "is_fixed": True,
    }
    response = client.post("/rooms", json=room, headers=headers)

    room = {
        "room": "string",
        "date_scheduled": "2025-02-06",
        "time_scheduled": "string",
        "type_scheduled": "extra",
    }
    response = client.post("/rooms", json=room, headers=headers)
    print(response.text)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "this scheduler is fixed"


def test_fixed_scheduler_already_exists(client):
    client.post(
        "/user/",
        json={
            "first_name": "bagriel",
            "last_name": "meula",
            "email": "teste@gmail.com",
            "password": "31324664",
        },
    )
    form_data = {"username": "teste@gmail.com", "password": "31324664"}
    token_response = client.post("/token", data=form_data)
    data = token_response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    profile = {
        "birth": "2002-12-29",
        "cpf": "string",
        "occupation": "string",
        "specialization": "string",
        "number_record": "string",
        "street": "string",
        "number": 0,
        "not_number": True,
        "neighborhood": "string",
        "city": "string",
        "cep": "string",
    }
    response = client.post("/users/profile", headers=headers, json=profile)
    room = {
        "room": "string",
        "date_scheduled": "2025-01-30",
        "time_scheduled": "string",
        "is_fixed": True,
    }
    response = client.post("/rooms", json=room, headers=headers)
    response = client.delete("/myrooms?item_id=1", headers=headers)
    room = {
        "room": "string",
        "date_scheduled": "2025-02-06",
        "time_scheduled": "string",
        "is_fixed": True,
    }
    response = client.post("/rooms", json=room, headers=headers)

    print(response.text)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "You Cant Scheduled this room"
