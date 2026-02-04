# init_db.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Role


def init_db():
    print("🔌 Conectando ao banco de dados...")
    db = SessionLocal()

    try:
        # Verifica se já existe alguma Role criada
        existing_role = db.query(Role).first()
        if existing_role:
            print("⚠️  As Roles já existem no banco. Nenhuma ação necessária.")
            return

        print("🚀 Criando roles padrão...")
        roles = [
            Role(description="Admin"),  # Deve assumir ID 1
            Role(description="Desenvolvedor"),  # Deve assumir ID 2
            Role(description="Gerente de Projetos"),  # Deve assumir ID 3
        ]

        db.add_all(roles)
        db.commit()
        print("✅ Sucesso! Roles inseridas no PostgreSQL.")

    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
