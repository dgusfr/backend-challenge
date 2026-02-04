import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------------------------------------------------------------
# [PASSO 1] Adicionar o diretório raiz ao path do Python
# Isso permite que o Alembic "enxergue" seus arquivos main.py, models.py, etc.
# ----------------------------------------------------------------------
sys.path.append(os.getcwd())

# ----------------------------------------------------------------------
# [PASSO 2] Importar seus Models e a URL do Banco
# Importamos o 'Base' do models.py para carregar a estrutura das tabelas
# Importamos a URL do database.py para usar a mesma conexão do Docker
# ----------------------------------------------------------------------
from models import Base
from database import SQLALCHEMY_DATABASE_URL

# Configuração do objeto de configuração do Alembic
config = context.config

# Interpreta o arquivo de log do alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------------------------------------------------
# [PASSO 3] Sobrescrever a URL do alembic.ini com a URL do seu código
# Isso garante que ele use o Postgres do Docker ou SQLite local dinamicamente
# ----------------------------------------------------------------------
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# Define os metadados para autogeração (Diz para o Alembic: "Olhe para estes modelos")
target_metadata = Base.metadata

# -- O restante do código abaixo é padrão do Alembic, não precisa mexer --


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'.

    Isso configura o contexto apenas com uma URL.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online'.

    Neste cenário, precisamos criar um Engine e associar uma conexão ao contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
