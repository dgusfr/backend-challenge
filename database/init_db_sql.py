import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()


sql_commands = """
INSERT INTO roles (description) VALUES ('Admin');
INSERT INTO roles (description) VALUES ('Desenvolvedor');
INSERT INTO roles (description) VALUES ('Gerente de Projetos');
"""

try:
    cursor.executescript(sql_commands)
    connection.commit()
    print("Sucesso! Roles inseridas via SQL.")
except sqlite3.OperationalError as e:
    print(f"Erro: {e}")
    print(
        "Provavelmente a tabela ainda não existe (rode o uvicorn antes) ou os dados já foram inseridos."
    )
finally:
    connection.close()
