import asyncio
from app.core.redis import get_redis
from app.db.database import get_db_pool
from app.workers.posting_status_worker import update_posting_status_worker

async def wait_for_db():
    while True:
        try:
            pool = await get_db_pool()
            return pool
        except Exception:
            print("Aguardando banco ficar disponível...")
            await asyncio.sleep(2)


async def main():
    print("Worker entrypoint iniciado")

    redis = get_redis()
    pool = await wait_for_db()

    print("Banco conectado, iniciando worker")
    await update_posting_status_worker(redis, pool)


if __name__ == "__main__":
    asyncio.run(main())
