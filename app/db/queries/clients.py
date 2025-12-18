CREATE_CLIENT = """
INSERT INTO clients (name, email, password)
VALUES ($1, $2, $3)
RETURNING id, name, email, created_at;
"""

SELECT_CLIENT_BY_EMAIL = """
SELECT id, name, email FROM clients WHERE email = $1;
"""

SELECT_CLIENTS = """
SELECT id, name, email FROM clients;
"""

DELETE_CLIENTS = """
DELETE FROM clients
WHERE id = $1;
"""