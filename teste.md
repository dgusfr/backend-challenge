┌─────────────────────────────────────────────────────────────────┐
│  1. DESENVOLVIMENTO (SEU COMPUTADOR)                           │
│     • Você escreve código                                       │
│     • Testa com docker-compose up                              │
│     • localhost:8000 (só você vê)                              │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                     git push origin main
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. GITHUB                                                      │
│     • Código armazenado                                         │
│     • Versionamento                                             │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                  GitHub Actions dispara
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. CI/CD (GITHUB ACTIONS)                                     │
│     • ✅ Roda testes (pytest)                                   │
│     • 🐳 Build da imagem Docker                                 │
│     • 📦 Push para Docker Hub/GHCR                              │
│     • 🚀 Conecta no servidor via SSH                            │
│     • 🔄 Atualiza containers no servidor                        │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                  docker pull nova imagem
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. SERVIDOR NA NUVEM (VPS/AWS/DO)                            │
│     IP: 142.93.45.123                                           │
│     • Docker rodando seus containers                            │
│     • PostgreSQL no container                                   │
│     • FastAPI no container                                      │
│     • API rodando na porta 8000                                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                     Nginx faz proxy
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. NGINX (PROXY REVERSO)                                      │
│     • Recebe requisições na porta 80/443                        │
│     • Adiciona HTTPS (SSL)                                      │
│     • Redireciona para localhost:8000                           │
└─────────────────────────────────────────────────────────────────┘
                           ↓
                     DNS resolve
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. INTERNET PÚBLICA                                            │
│     https://api.seudominio.com                                  │
│     • Qualquer pessoa no mundo pode acessar                     │
│     • API disponível 24/7                                       │
└─────────────────────────────────────────────────────────────────┘



---

## ✅ Executando Testes

O projeto possui testes automatizados de infraestrutura e regras de negócio utilizando `pytest` com banco de dados em memória (isolado).

```bash
pytest 

```

<img src="images/image copy 2.png" alt="Pytest" width="800"/>

## Consumindo a API (Postman/Insomnia)

é posisvel importar o arquivo **`docs/openapi.yaml`** no Postman ou Insomnia para facilitar os testes das rotas.

<img src="images/image.png" alt="postman" width="800"/>

<img src="images/image copy.png" alt="postman" width="800"/>

---

## 📖 Documentação da API

Você pode visualizar a especificação da API de duas formas:

1. **Swagger UI (Online):**
Com a API rodando, acesse: `http://localhost:8000/docs`

<img src="images/image copy 5.png" alt="Swagger UI" width="800"/>

2. **Documentação Offline (Para Postman/Insomnia):**
O arquivo de especificação OpenAPI (Swagger) está disponível no repositório em:
📂 **`docs/openapi.yaml`**

* **Como usar:** Importe este arquivo diretamente no Postman ou no [Swagger Editor](https://editor.swagger.io/) para visualizar os contratos, schemas e testar as rotas sem precisar rodar o código Python.


comando para inicar servidor local
uvicorn main:app --reload --host