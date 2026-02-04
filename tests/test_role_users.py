def test_create_user(client):
    """Cria usuário e verifica se o ID e a Role retornam certos"""
    resp = client.post(
        "/users/", json={"name": "Leo", "email": "leo@test.com", "role_id": 1}
    )
    assert resp.status_code == 201
    assert resp.json()["role"]["description"] == "Admin"


def test_get_user_role(client):
    """Cria user, busca endpoint de role específica e valida retorno"""
    user_id = client.post(
        "/users/", json={"name": "Ana", "email": "ana@test.com", "role_id": 2}
    ).json()["id"]

    # Testa o endpoint alvo
    resp = client.get(f"/users/{user_id}/role")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Dev"
