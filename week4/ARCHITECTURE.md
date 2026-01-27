# DAY 1 — NODE + PROJECT ARCHITECTURE

This project follows a clean, layered architecture to ensure scalability, maintainability, and separation of concerns.

## Directory Structure

- `src/config/`: Configuration management (env variables, constants).
  - `index.js`: Environment-based config loader with fallback support
- `src/loaders/`: Bootstrapping logic (Express, MongoDB, Routes, etc.).
  - `app.js`: Express application setup and middleware configuration
  - `db.js`: Database connection initialization
  - `routes.js`: Route mounting and dynamic endpoint counting
- `src/models/`: Database schemas and models (Mongoose/Sequelize).
- `src/routes/`: API route definitions.
- `src/controllers/`: Request handling and response formatting.
- `src/services/`: Business logic layer.
- `src/repositories/`: Data access layer (abstraction over DB).
- `src/middlewares/`: Express custom middlewares (auth, validation).
- `src/utils/`: Shared utility functions (logger, helpers).
  - `logger.js`: Winston-based centralized logging with file and console transports
- `src/jobs/`: Background tasks and cron jobs.
- `src/logs/`: Application log files (error.log, combined.log).

## Application Startup Flow

The application starts in the following order:

1. Environment configuration is loaded.
2. Logger is initialized.
3. Database connection is established.
4. Express application is initialized.
5. Global middlewares are applied.
6. API routes are mounted and total endpoint count is logged.
7. Global error handlers are registered.
8. Server starts listening on the configured port.

Startup orchestration is handled from `src/index.js` using loaders.


