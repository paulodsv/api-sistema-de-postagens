import json
from fastapi import HTTPException
import logging
from app.db.queries.postings import UPDATE_POSTING_STATUS

logger = logging.getLogger("posting_worker")
logging.basicConfig(level=logging.INFO)



async def update_posting_status_worker(redis, pool):
    status_list = ["pending", "shipped", "delivered"]

    while True:
        print("🟢 Worker aguardando job...")
        try:
            _, job = await redis.blpop("posting_status_queue")
            data = json.loads(job)
            posting_id = data["posting_id"]
            new_status = data["new_status"]

            async with pool.acquire() as conn:
                async with conn.transaction():
                    current_status = await conn.fetchrow("SELECT status FROM postings WHERE id = $1;", posting_id)

                    if not current_status: #Se não existir o valor status pra esse posting id = invalid entry
                        logger.warning(f"Posting {posting_id} not found")
                        continue
                        
                    if current_status["status"] == new_status: #Se o status atual for igual ao novo status informado = invalid entry
                        logger.info(f"Posting {posting_id} already updated")
                        continue
                        
                    current_status_index = status_list.index(current_status["status"])
                    new_status_index = status_list.index(new_status)

                    if new_status_index < current_status_index: #Se a entrada pro novo status for um status anterior do atual = invalid entry
                        logger.warning(f"Invalid status regression for {posting_id}")
                        continue
                    
                    old_status = current_status["status"]

                    updated = await conn.fetchrow(UPDATE_POSTING_STATUS, new_status, posting_id) 
                        
                    await conn.execute(
                        "INSERT INTO  status_history (posting_id, old_status, new_status) VALUES ($1, $2, $3);", posting_id, old_status, new_status
                        )
                        
                    if new_status == "shipped":
                        await conn.execute(
                            "UPDATE postings SET shipped_at = NOW() WHERE id = $1", posting_id
                        )

                    if new_status == "delivered":
                        await conn.execute(
                            "UPDATE postings SET delivered_at = NOW() WHERE id = $1", posting_id
                        )

        except Exception as e:
            logger.exception(f"Error processing job: {e}")
