# 1. SELECT
query = session.query(
    User.name,
    User.email,
    Role.description.label(
        "role"
    ),  # label = nome alternativo para a coluna no resultado
    Claim.description.label("claim"),
)

# 2. INNER JOIN
# (tabela alvo, condição de junção)
query = query.join(Role, User.role_id == Role.id)

# 3. O JOIN opcional com a tabela pivô (o 1º LEFT JOIN)
# Nota: "outerjoin" é o nome do SQLAlchemy para LEFT JOIN
query = query.outerjoin(
    user_claims, User.id == user_claims.c.user_id
)  # .c = coluna da tabela pivô

# 4. º LEFT JOIN
query = query.outerjoin(Claim, user_claims.c.claim_id == Claim.id)

# 5. Executar a consulta
results = query.all()

# ===========================

# No padrão SQLAlchemy 2.0

from sqlalchemy import select

statements = (
    select(
        User.name,
        User.email,
        Role.description.label("role"),
        Claim.description.label("claim"),
    )
    .join(Role, User.role_id == Role.id)
    .outerjoin(UserClaim, User.id == UserClaim.user_id)
    .outerjoin(Claim, UserClaim.claim_id == Claim.id)
)

rows = session.execute(statements).all()
# rows -> lista de Row (tuplas): [(name, email, role, claim), ...]
