const express = require('express');
const Logger = require('../utils/logger');
const { errorHandler, notFoundHandler } = require('../middlewares/error.middleware');

module.exports = ({ app }) => {
    app.use(express.json());

    Logger.info('Middlewares loaded');

    const routeCount = require('./routes')({ app });
    Logger.info(`Routes mounted: ${routeCount} endpoints`);

    // 404 handler
    app.use(notFoundHandler);

    // Global error handler
    app.use(errorHandler);
};
