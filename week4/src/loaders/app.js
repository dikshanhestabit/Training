const express = require('express');
const Logger = require('../utils/logger');

module.exports = ({ app }) => {
    app.use(express.json());

    Logger.info('Middlewares loaded');

    const routeCount = require('./routes')({ app });
    Logger.info(`Routes mounted: ${routeCount} endpoints`);

    // 404 handler
    app.use((req, res, next) => {
        const err = new Error('Not Found');
        err['status'] = 404;
        next(err);
    });

    // Global error handler
    app.use((err, req, res, next) => {
        res.status(err.status || 500);
        res.json({
            errors: {
                message: err.message,
            },
        });
    });
};
