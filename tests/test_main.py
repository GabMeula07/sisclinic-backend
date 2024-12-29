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
