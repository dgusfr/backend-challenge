#  API de Controle de Acesso

API REST desenvolvida em Python com **FastAPI** para gerenciamento de usuários e controle de acesso baseado em Roles.

O projeto foi construído seguindo princípios de **Clean Code**, **Arquitetura em Camadas** e **Testes Automatizados**, preparado para escalar de um ambiente local simples para uma arquitetura produtiva containerizada.

## 🛠 Tecnologias Utilizadas

* **Framework:** FastAPI
* **Servidor (Dev):** Uvicorn
* **Servidor (Prod):** Gunicorn gerenciando Uvicorn workers
* **Banco de Dados:** SQLite (Ambiente Local) / Suporte a PostgreSQL (Produção)
* **ORM:** SQLAlchemy
* **Testes:** Pytest
* **Infraestrutura:** Docker & Docker Compose

---

## Como Executar Localmente 

Recomendado para desenvolvimento rápido e depuração.

### 1. Pré-requisitos
* Git
* Python 3.10 
* Pip

### 2. Instalação

Clone o repositório e entre na pasta:
```bash
git clone [https://github.com/dgusfr/backend-challenge.git](https://github.com/dgusfr/backend-challenge.git)
cd backend-challenge

```

Crie e ative o ambiente virtual:

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows 
python -m venv venv
.\venv\Scripts\activate

```

Instale as dependências:

```bash
pip install -r requirements.txt

```

### 3. Rodar a Aplicação

Inicie o servidor em modo de desenvolvimento (com auto-reload):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

Acesse: `http://localhost:8000`

### 4. Endpoints Principais

Consumir os endpoint para criar usuários e retornar roles via postman ou insomnia


---

## Deploy em Produção

Perfeito! Agora vejo sua estrutura. Você tem **todos os arquivos Python na raiz** do projeto e já criou alguns arquivos Docker! Vou adaptar tudo para sua estrutura específica.

### **1. Dockerfile** 

```dockerfile
FROM python:3.11-slim

WORKDIR /code

# Copia requirements primeiro (cache do Docker)
COPY ./requirements.txt /code/requirements.txt

# Instala dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia TODOS os arquivos Python da raiz
COPY ./main.py /code/main.py
COPY ./database.py /code/database.py
COPY ./models.py /code/models.py
COPY ./schemas.py /code/schemas.py

# Se tiver outras pastas necessárias, copie também
# COPY ./query /code/query
# COPY ./database /code/database

EXPOSE 8000

# Como seu main.py está na raiz, use "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

***

### **2. docker-compose.yml**

```yaml
version: '3.8'

services:
  # Serviço PostgreSQL
  db:
    image: postgres:15
    container_name: fastapi_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fastapi_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - fastapi-network

  # Serviço FastAPI
  api:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - fastapi-network

volumes:
  postgres_data:

networks:
  fastapi-network:
    driver: bridge
```

***

### **3. .dockerignore** 

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/
env/
.git
.gitignore
.pytest_cache
.coverage
*.log
.env
.env.local
*.db
*.sqlite
*.sqlite3
test.db
tests/
test/
docs/
images/
.DS_Store
```


***

### **4. Verificar requirements.txt**

Seu `requirements.txt` deve ter:

```txt
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
```

Se não tiver `psycopg2-binary`, instale:

```bash
pip install psycopg2-binary
pip freeze > requirements.txt
```

***


### **Passo 5: Build e Subir os Containers**

```bash
# Build das imagens
docker-compose build

# Subir os containers
docker-compose up -d
```

**O que vai acontecer:**
- Docker vai baixar PostgreSQL 15
- Vai construir sua API com os arquivos da raiz
- Vai criar 2 containers: `fastapi_db` e `fastapi_app`

***

### **Passo 6: Verificar se Está Rodando**

```bash
# Ver containers rodando
docker-compose ps

# Ver logs
docker-compose logs -f
```

**Você deve ver:**
```
NAME            STATUS    PORTS
fastapi_db      running   0.0.0.0:5432->5432/tcp
fastapi_app     running   0.0.0.0:8000->8000/tcp
```

***

## Passo  7: Deploy na AWS EC2 (Produção)

### ** 7.1: Criar Instância EC2 na AWS**

***

### ** 7.2: Conectar na EC2 via SSH**

No seu terminal local: [dev](https://dev.to/goodluck_ekeoma_2c98866d0/containerizing-and-deploying-a-simple-fastapi-application-to-aws-ec2-pa2)

```bash
# Dar permissão na chave
chmod 400 fastapi-key.pem

# Conectar na EC2 (substitua o IP)
ssh -i fastapi-key.pem ubuntu@SEU-IP-PUBLICO

# Exemplo:
# ssh -i fastapi-key.pem ubuntu@54.123.45.67
```

***

### ** 7.3: Instalar Docker e Docker Compose na EC2**

Dentro da EC2, execute estes comandos: [youtube](https://www.youtube.com/watch?v=9AA0gKmcxNM)

```bash
# Atualizar pacotes
sudo apt update

# Instalar Docker
sudo apt install -y docker.io

# Habilitar Docker para iniciar com o sistema
sudo systemctl enable --now docker

# Adicionar seu usuário ao grupo docker (para não precisar de sudo)
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install -y docker-compose

# Verificar instalação
docker --version
docker-compose --version

# IMPORTANTE: Fazer logout e login novamente para aplicar permissões
exit
```

Conecte novamente:
```bash
ssh -i fastapi-key.pem ubuntu@SEU-IP-PUBLICO
```

***

### ** 7.4: Enviar Código para EC2**

**Via GitHub** [dev](https://dev.to/theinfosecguy/how-to-deploy-a-fastapi-application-using-docker-on-aws-4m61)

Se seu código está no GitHub:

```bash
# Na EC2, clonar seu repositório
git clone https://github.com/dgusfr/backend-challenge.git
cd backend-challenge
```

***

### ** 7.5: Configurar Variáveis de Ambiente para Produção**

Na EC2, crie/edite o arquivo `.env`: [dev](https://dev.to/shaikhalamin/how-to-deploy-fastapi-app-with-postgresql-database-in-aws-ec2-2hn5)

```bash
# Na EC2
nano .env
```

Cole este conteúdo:

```bash
DATABASE_URL=postgresql://postgres:postgres_prod_2026@db:5432/fastapi_db
SECRET_KEY=sua-chave-super-secreta-aqui-mude-isso
DEBUG=False
```

**Pressione:** `Ctrl + O` → Enter → `Ctrl + X`

***

### **7.6: Subir os Containers em Produção**

```bash
# Build das imagens
docker-compose build

# Subir em modo detached (background)
docker-compose up -d

# Ver se está rodando
docker-compose ps

# Ver logs
docker-compose logs -f
```

***

### **7.7: Criar Tabelas no Banco**

Na EC2: [dev](https://dev.to/goodluck_ekeoma_2c98866d0/containerizing-and-deploying-a-simple-fastapi-application-to-aws-ec2-pa2)

```bash
docker-compose exec api python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

***

### **7.8: Testar a API em Produção**

No seu navegador, acesse:

```
http://SEU-IP-PUBLICO:8000/docs
```

Exemplo:
```
http://54.123.45.67:8000/docs
```

Você deve ver o Swagger da sua API rodando na nuvem! [dev](https://dev.to/theinfosecguy/how-to-deploy-a-fastapi-application-using-docker-on-aws-4m61)

**Teste via curl:**
```bash
curl http://SEU-IP-PUBLICO:8000/docs
```

***