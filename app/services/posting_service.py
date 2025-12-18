import json
from fastapi import HTTPException, Request
from app.models.postings import CreatePosting, PostStatus
from app.core.utils import calculate_freight, generate_tracking_code
from app.db.queries.postings import CREATE_POSTINGS, SELECT_POSTING_BY_TRACKING_CODE, UPDATE_POSTING_STATUS, DELETE_POSTING
from app.db.database import get_db_pool

import asyncpg

async def create_posting_service(posting: CreatePosting):
    pool = await get_db_pool()
    frete = calculate_freight(posting.weight_kg, posting.volume_cm3)
    tracking_code = generate_tracking_code()

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    CREATE_POSTINGS,
                    posting.client_id,
                    posting.description,
                    posting.weight_kg, 
                    posting.volume_cm3,
                    frete,
                    tracking_code
                    )
                return dict(row)

    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail = "Postagem já registrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Erro interno ao tentar criar uma nova postagem. Error: {str(e)}")
    

async def get_posting_by_tracking_code_service(tracking_code: str):
    pool = await get_db_pool()
    row = await pool.fetchrow(SELECT_POSTING_BY_TRACKING_CODE, tracking_code)

    if not row:
        raise HTTPException(status_code=404, detail="Código de rastreio não encontrado.")
    
    return dict(row)


async def update_posting_status_service(posting_id: int, new_status: PostStatus, request: Request):
    redis = request.app.state.redis
    
    payload = {
        "posting_id": posting_id,
        "new_status": new_status.value
    }

    await redis.rpush(
        "posting_status_queue",
        json.dumps(payload)
    )

    return {
        "message": "Status update accepted for processing",
        "posting_id": posting_id,
        "new_status": new_status.value
    }

async def delete_posting_by_id_service(id: int):
    pool = await get_db_pool()
    row = await pool.fetchrow(DELETE_POSTING, id)

    if not row:
        raise HTTPException(status_code=404, detail="Postagem não encontrada.")

    return {"deleted": True}

