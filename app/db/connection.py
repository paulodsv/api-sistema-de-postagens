from fastapi import FastAPI
from app.db.database import get_db_pool
from app.core.redis import get_redis
import asyncio


async def wait_for_db():
    while True:
        try:
            pool = await get_db_pool()
            return pool
        except Exception:
            print("⏳ Aguardando banco ficar disponível...")
            await asyncio.sleep(2)


async def connect_to_db(app: FastAPI):
    print("[DB] Criando pool de conexões...")
    app.state.db = await wait_for_db()
    print("[DB] Pool criada e salva em app.state.db")

    app.state.redis = get_redis()

async def close_connection_to_db(app: FastAPI):
    print("[DB] Fechando pool de conexões...")
    await app.state.db.close()
    print("[DB] Pool encerrada")

