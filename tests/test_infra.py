def test_app_is_alive(client):
    """Verifica se a API responde (mesmo que 404)"""
    assert client.get("/").status_code == 404


def test_database_integration(client):
    """Tenta buscar uma Role para garantir que o banco em memória subiu"""
    assert client.get("/roles/1").status_code == 200
