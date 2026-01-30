const logger = require('../utils/logger');

/**
 * Custom Error Classes
 */
class AppError extends Error {
    constructor(message, statusCode, code) {
        super(message);
        this.statusCode = statusCode;
        this.code = code;
        this.isOperational = true;
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends AppError {
    constructor(message) {
        super(message, 400, 'VALIDATION_ERROR');
    }
}

class NotFoundError extends AppError {
    constructor(message) {
        super(message, 404, 'NOT_FOUND');
    }
}

class DatabaseError extends AppError {
    constructor(message) {
        super(message, 500, 'DATABASE_ERROR');
    }
}

/**
 * Global Error Handler Middleware
 */
const errorHandler = (err, req, res, next) => {
    // Default error values
    let statusCode = err.statusCode || 500;
    let message = err.message || 'Internal Server Error';
    let code = err.code || 'INTERNAL_ERROR';

    // Handle Mongoose validation errors
    if (err.name === 'ValidationError') {
        statusCode = 400;
        code = 'VALIDATION_ERROR';
        message = Object.values(err.errors)
            .map(e => e.message)
            .join(', ');
    }

    // Handle Mongoose CastError (invalid ObjectId)
    if (err.name === 'CastError') {
        statusCode = 400;
        code = 'INVALID_ID';
        message = 'Invalid ID format';
    }

    // Handle Mongoose duplicate key error
    if (err.code === 11000) {
        statusCode = 409;
        code = 'DUPLICATE_ENTRY';
        const field = Object.keys(err.keyPattern)[0];
        message = `${field} already exists`;
    }

    // Log error
    logger.error({
        message: err.message,
        code,
        statusCode,
        stack: err.stack,
        path: req.path,
        method: req.method,
    });

    // Send error response
    res.status(statusCode).json({
        success: false,
        message,
        code,
        timestamp: new Date().toISOString(),
        path: req.path,
    });
};

/**
 * 404 Not Found Handler
 */
const notFoundHandler = (req, res, next) => {
    res.status(404).json({
        success: false,
        message: `Route ${req.originalUrl} not found`,
        code: 'ROUTE_NOT_FOUND',
        timestamp: new Date().toISOString(),
        path: req.path,
    });
};

module.exports = {
    AppError,
    ValidationError,
    NotFoundError,
    DatabaseError,
    errorHandler,
    notFoundHandler,
};
