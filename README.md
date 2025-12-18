# 📦 Sistema de Postagens – API Assíncrona com FastAPI, Redis e PostgreSQL

Este projeto é uma **API REST para gerenciamento de postagens logísticas**, desenvolvida em **Python** com foco em **arquitetura backend, concorrência e processamento assíncrono**.

A aplicação permite cadastrar clientes, criar postagens, consultar envios por código de rastreamento e atualizar o status logístico de forma segura e escalável, utilizando **Redis como fila** e um **worker dedicado** para processamento assíncrono.

---

## 🚀 Funcionalidades

- Cadastro de clientes
- Autenticação de clientes
- Criação de postagens vinculadas a clientes
- Geração automática de código de rastreamento único
- Consulta de postagens por código de rastreamento
- Atualização de status logístico (`pending`, `shipped`, `delivered`)
- Registro de histórico de alterações de status
- Processamento assíncrono de atualizações via fila Redis

---

## 🧠 Arquitetura e decisões técnicas

- **FastAPI** para criação da API REST
- **PostgreSQL** como banco de dados relacional
- **SQL puro** com `asyncpg` (sem ORM)
- **Redis** utilizado como fila de mensagens
- **Worker assíncrono** separado da API para consumo da fila
- **Docker Compose** para orquestração dos serviços
- **Persistência de dados** com volumes Docker
- **Integridade garantida no banco** através de constraints (`PRIMARY KEY`, `UNIQUE`, `FOREIGN KEY`, `CHECK`)
- **Desacoplamento entre endpoints e serviços**, evitando dependência direta do framework

---


## 🗂️ Estrutura do projeto

A estrutura do projeto foi organizada para garantir **separação clara de responsabilidades**, **baixo acoplamento** e **facilidade de manutenção**, seguindo um fluxo unidirecional entre as camadas.

```
app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── routes_clients.py
│           │   └── Endpoints HTTP de clientes
│           │       → chamam services.clients_service
│           │
│           └── routes_postings.py
│               └── Endpoints HTTP de postagens
│                   → chamam services.posting_service
│
├── core/
│   ├── auth.py
│   │   └── Autenticação e geração de tokens
│   │
│   ├── deps.py
│   │   └── Dependências compartilhadas da aplicação
│   │
│   ├── redis.py
│   │   └── Configuração do cliente Redis assíncrono
│   │
│   └── utils.py
│       └── Funções utilitárias (helpers)
│
├── db/
│   ├── connection.py
│   │   └── Ciclo de vida das conexões (startup / shutdown)
│   │
│   ├── database.py
│   │   └── Criação e gerenciamento do pool asyncpg
│   │
│   └── queries/
│       ├── clients.py
│       │   └── Consultas SQL puras (clientes)
│       │
│       └── postings.py
│           └── Consultas SQL puras (postagens)
│
├── models/
│   ├── clients.py
│   │   └── Modelos e schemas de clientes
│   │
│   └── postings.py
│       └── Modelos e schemas de postagens
│
├── services/
│   ├── clients_service.py
│   │   └── Regras de negócio de clientes
│   │
│   └── posting_service.py
│       └── Regras de negócio de postagens
│           
│
├── workers/
│   └── posting_status_worker.py
│       └── Worker assíncrono
│           → consome fila Redis
│           → atualiza banco de dados
│
├── worker.py
│   └── Entry point do worker
│
├── main.py
│   └── Entry point da API FastAPI
│       → registra routers
│       → inicializa DB e Redis
│
├── config.py
│   └── Leitura e validação de variáveis de ambiente
│
└── __init__.py
```

---

## 🧠 Princípios adotados

* `api` **não acessa banco diretamente**
* `services` **não dependem do FastAPI**
* `queries` contêm **apenas SQL**
* `workers` reutilizam regras e infraestrutura
* `core` centraliza autenticação e Redis
* Dependências fluem **sempre para dentro**
  
---

## 🔄 Processamento assíncrono

A atualização de status das postagens não é feita diretamente pela API.  
Ao receber a requisição:

1. A API valida os dados
2. Enfileira a solicitação no Redis
3. Retorna imediatamente uma resposta ao cliente
4. Um worker consome a fila e processa a atualização no banco

Esse modelo evita bloqueio de requisições HTTP e prepara o sistema para escalar processamento.

---

## 🐳 Infraestrutura

O projeto utiliza Docker para execução local:

### Serviços
- `api`: FastAPI
- `worker`: consumidor da fila Redis
- `db`: PostgreSQL
- `redis`: fila de mensagens

---

## ▶️ Como executar o projeto

### Pré-requisitos
- Docker
- Docker Compose

### Subir a aplicação
```bash
docker-compose up --build
