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
