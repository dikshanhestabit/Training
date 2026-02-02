const { AsyncLocalStorage } = require('async_hooks');
const { randomUUID } = require('crypto');

const asyncLocalStorage = new AsyncLocalStorage();

// Middleware to generate and attach a request ID //
const tracingMiddleware = (req, res, next) => {
    const requestId = req.get('X-Request-ID') || randomUUID();

    // Attach to response header for debugging
    res.setHeader('X-Request-ID', requestId);

    // Store in context
    asyncLocalStorage.run({ requestId }, () => {
        next();
    });
};

// Get the current request ID from context //
const getRequestId = () => {
    const store = asyncLocalStorage.getStore();
    return store ? store.requestId : null;
};

module.exports = {
    tracingMiddleware,
    getRequestId,
};
