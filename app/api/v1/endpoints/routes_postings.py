from fastapi import APIRouter, Depends
from app.models.postings import CreatePosting, PostStatus
from fastapi import Request
from app.services.posting_service import create_posting_service, get_posting_by_tracking_code_service, update_posting_status_service, delete_posting_by_id_service
from app.core.deps import get_current_client

router = APIRouter(prefix="/postings", tags=["Postings"])

@router.post("/", dependencies=[Depends(get_current_client)])
async def create_posting(posting: CreatePosting):
    return await create_posting_service(posting)

@router.get("/{tracking_code}", dependencies=[Depends(get_current_client)])
async def get_posting_by_tracking_code(tracking_code: str):
    return await get_posting_by_tracking_code_service(tracking_code)

@router.put("/status/{posting_id}", dependencies=[Depends(get_current_client)])
async def update_posting_status(posting_id: int, new_input_status: PostStatus, request: Request):
    return await update_posting_status_service(posting_id, new_input_status, request)

@router.delete("/{posting_id}", dependencies=[Depends(get_current_client)])
async def delete_posting_by_id(id: int):
    return await delete_posting_by_id_service(id)