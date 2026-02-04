# Service Architecture

A three-tier multi-container application orchestrated by **Docker Compose**.

## Services
- **Frontend (Client)**: Minimal React app served at `localhost:5173`.
- **Backend (Server)**: Node/Express API at `localhost:5000`.
- **Database (MongoDB)**: Data store mapped to host port `27018`.

## Core Requirements Verified
- **Networking**: All containers share a default bridge network. The Server connects to Mongo using the hostname `mongodb`.
- **Persistence**: A named volume `mongo-data` is mapped to `/data/db` for database storage.
- **Logging**: Service logs are accessible via `docker compose logs`.
- **One-Command Setup**: Deployment handled entirely via `docker compose up -d`.
