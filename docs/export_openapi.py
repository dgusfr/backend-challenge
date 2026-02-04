import yaml
import sys
import os

# 1. Ajusta o path ANTES de importar o app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
from fastapi.openapi.utils import get_openapi


openapi_schema = get_openapi(
    title="API de Controle de Acesso",
    version="1.0.0",
    description="API para gestão de Usuários e Roles",
    routes=app.routes,
)

file_path = os.path.join(current_dir, "openapi.yaml")

with open(file_path, "w", encoding="utf-8") as f:
    yaml.dump(openapi_schema, f, default_flow_style=False, allow_unicode=True)

print(f"Arquivo gerado com sucesso em: {file_path}")
