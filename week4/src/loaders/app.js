const express = require('express');
const Logger = require('../utils/logger');
const { errorHandler, notFoundHandler } = require('../middlewares/error.middleware');
const { setupPreSecurity, setupPostSecurity } = require('../middlewares/security');

module.exports = ({ app }) => {
    // 1. Pre-Processing Security (Helmet, CORS, RateLimit)
    setupPreSecurity(app);

    // 2. Body Parsing (with Size Limit)
    app.use(express.json({ limit: '10kb' }));

    // 3. Post-Processing Security (Sanitization)
    setupPostSecurity(app);

    Logger.info('Middlewares loaded');

    const routeCount = require('./routes')({ app });
    Logger.info(`Routes mounted: ${routeCount} endpoints`);

    // 404 handler
    app.use(notFoundHandler);

    // Global error handler
    app.use(errorHandler);
};
