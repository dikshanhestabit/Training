# Deployment Notes 

## Prerequisites
- Node.js v18+
- Redis Server (Optional, set `REDIS_USE_MOCK=true` if not available)
- MongoDB Server

## Getting Started
1. Clone the repository.
2. Run `npm install`.
3. Copy `.env.example` to `.env` and configure your variables.
4. Run `npm start` for production or `npm run dev` for development.

## Process Management (PM2)
The application is pre-configured for PM2.
```bash
# Start with PM2
pm2 start ecosystem.config.js

# Monitor logs
pm2 logs

# Monitor processes
pm2 status
```

## Logging
Logs are stored in the `/src/logs` directory:
- `combined.log`: All logs with request IDs.
- `error.log`: Only error-level logs.

## Background Jobs
Background jobs (email notifications) are handled by BullMQ.
In development, an in-memory Redis mock is used if no real Redis is found.
