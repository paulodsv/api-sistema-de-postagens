from fastapi import HTTPException
from app.db.queries.clients import CREATE_CLIENT, SELECT_CLIENT_BY_EMAIL, SELECT_CLIENTS, DELETE_CLIENTS
from app.models.clients import CreateClient
from app.core.auth import create_access_token, create_refresh_token
from app.db.database import get_db_pool

import asyncpg


async def create_client_service(client: CreateClient):
    pool = await get_db_pool()
    
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    CREATE_CLIENT,
                    client.name,
                    client.email,
                    client.password
                )
                return dict(row)
            
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail = "Cliente já cadastrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Erro interno ao tentar criar cliente. Erro: {str(e)}")
    
    
async def client_login_service(email: str, password: str):
    pool = await get_db_pool()

    row = await pool.fetchrow("SELECT id, name, password FROM clients WHERE email = $1", email)
    if not row:
        raise HTTPException(status_code=404, detail="Email não encontrado.")

    if row["password"] != password:
        raise HTTPException(status_code=402, detail="Senha incorreta.")
    
    payload = {
        "sub": str(row["id"]),
        "name": row["name"],
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
async def get_client_by_email_service(email: str):
    pool = await get_db_pool()
    row = await pool.fetchrow(SELECT_CLIENT_BY_EMAIL, email)

    if not row:
        raise HTTPException(status_code=404, detail="Este e-mail não está vinculado a um usuário.")

    return dict(row)


async def list_clients_service():
    pool = await get_db_pool()
    rows = await pool.fetch(SELECT_CLIENTS)

    return [dict(r) for r in rows]


async def delete_client_by_id_service(id: int):
    pool = await get_db_pool()

    try:
        return await pool.execute(DELETE_CLIENTS, id)
    
    except Exception as e:
        raise HTTPException(status_code=404, detail= f"Erro ao deletar id {id}. Erro: {str(e)}")