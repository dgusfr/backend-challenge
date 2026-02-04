CREATE TABLE roles (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY, -- Gerar automaticamente um número sequencial para esta coluna (auto-incremento), não é necessário inserir manualmente.
	description varchar NOT NULL, -- varchar: Define que a coluna armazenará texto de tamanho variável.
	CONSTRAINT roles_pk PRIMARY KEY -- (id) Define qual coluna será o identificador único e exclusivo de cada registro na tabela.
);

CREATE TABLE claims (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	description varchar NOT NULL,
	active bool NOT NULL DEFAULT true,
	CONSTRAINT claims_pk PRIMARY KEY (id)
);

CREATE TABLE users (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar NOT NULL,
	email varchar NOT NULL,
	"password" varchar NOT NULL,
	role_id int4 NOT NULL,
	created_at date NOT NULL,
	updated_at date NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);

ALTER TABLE users ADD CONSTRAINT users_fk FOREIGN KEY (role_id) REFERENCES roles(id); -- ALTER TABLE: Modifica uma tabela users, já existente criando uma relação de chave estrangeira (FOREIGN KEY) entre a coluna role_id da tabela users e a coluna id da tabela roles.

CREATE TABLE user_claims (
	user_id int8 NOT NULL,
	claim_id int8 NOT NULL,
	CONSTRAINT user_claims_un UNIQUE (user_id, claim_id) -- Garante que a combinação de user_id e claim_id seja única na tabela user_claims.
);

ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk_1 FOREIGN KEY (claim_id) REFERENCES claims(id);


---------------------------------------------------

SELECT
  u."name",
  u.email,
  r.description AS role,
  c.description AS claim
FROM users u
JOIN roles r ON u.role_id = r.id
LEFT JOIN user_claims uc ON u.id = uc.user_id
LEFT JOIN claims c ON uc.claim_id = c.id;


# Nessa query o usuario vai ser repetido por linha de claim que ele possuir
# Se um usuario tiver 3 claims, ele vai aparecer 3 vezes na consulta, uma para cada claim