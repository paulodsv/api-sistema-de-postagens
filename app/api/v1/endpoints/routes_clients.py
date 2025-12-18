from fastapi import APIRouter
from app.models.clients import CreateClient
from fastapi import Request
from app.services.clients_service import create_client_service, get_client_by_email_service, list_clients_service, delete_client_by_id_service, client_login_service
from fastapi import Depends
from app.core.deps import get_current_client


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/register")
async def client_register(client: CreateClient):
    return await create_client_service(client)


@router.post("/login")
async def client_login(email: str, password: str):
    return await client_login_service(email, password)



@router.get("/", dependencies=[Depends(get_current_client)])
async def get_clients():
    return await list_clients_service()


@router.get("/{client_email}", dependencies=[Depends(get_current_client)])
async def get_client_by_email(client_email: str):
    return await get_client_by_email_service(client_email)



@router.delete("/{user_id}", dependencies=[Depends(get_current_client)])
async def delete_client_by_id(user_id: int):
    return await delete_client_by_id_service(user_id)








