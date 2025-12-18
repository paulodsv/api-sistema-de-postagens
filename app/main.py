from app.db.connection import connect_to_db, close_connection_to_db
from fastapi import FastAPI
from app.api.v1.endpoints.routes_clients import router as clients_router
from app.api.v1.endpoints.routes_postings import router as postings_router


app = FastAPI(title="Sistema de Postagens com FastAPI", description="O Sistema de Postagens é uma API destinada" \
                    " ao gerenciamento de envios de encomendas. Ele permite cadastrar clientes, criar postagens associadas a esses clientes" \
                    " e acompanhar todo o fluxo logístico de cada envio. Ao registrar uma postagem, a API calcula automaticamente o valor do frete " \
                    "com base no peso e volume informados e gera um código de rastreamento único no formato “PKG-XXXXXXXXXXXX”. Cada postagem inicia " \
                    "com o status “pending”, podendo ser atualizada para “shipped” ou “delivered”, com os respectivos horários registrados automaticamente. " \
                    "Todas as alterações de status são auditadas na tabela de histórico, permitindo o acompanhamento completo da trajetória de cada encomenda. " \
                    "O sistema utiliza FastAPI, PostgreSQL, Docker e SQL puro via asyncpg, seguindo uma arquitetura modular baseada em endpoints, serviços e consultas SQL.")



@app.on_event("startup")
async def on_start():
    await connect_to_db(app)

@app.on_event("shutdown")
async def on_shutdown():
    await close_connection_to_db(app)

app.include_router(clients_router)
app.include_router(postings_router)
