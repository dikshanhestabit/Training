const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');
const hpp = require('hpp');
const Logger = require('../utils/logger');

const setupPreSecurity = (app) => {
    // 1. Set security HTTP headers
    app.use(helmet());

    // 2. Enable CORS
    app.use(cors());

    // 3. Rate Limiting
    const limiter = rateLimit({
        windowMs: 15 * 60 * 1000, // 15 minutes
        max: 100, // Limit each IP to 100 requests per windowMs
        message: 'Too many requests from this IP, please try again in 15 minutes',
        handler: (req, res, next, options) => {
            Logger.warn(`Rate limit exceeded for IP: ${req.ip}`);
            res.status(options.statusCode).send(options.message);
        },
        standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
        legacyHeaders: false, // Disable the `X-RateLimit-*` headers
    });

    // Apply to all requests
    app.use(limiter);

    Logger.info('Pre-processing security middleware applied: Helmet, CORS, RateLimit');
};

const setupPostSecurity = (app) => {
    // 4. Data Sanitization against NoSQL query injection
    app.use((req, res, next) => {
        if (req.body) req.body = mongoSanitize.sanitize(req.body);
        if (req.params) req.params = mongoSanitize.sanitize(req.params);
        try {
            if (req.query) req.query = mongoSanitize.sanitize(req.query);
        } catch (err) {
            // Ignore if req.query is read-only
        }
        next();
    });

    // 5. Custom Data Sanitization against XSS
    app.use((req, res, next) => {
        const clean = (data) => {
            if (typeof data === 'string') {
                return data.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            }
            if (data && typeof data === 'object') {
                Object.keys(data).forEach(key => {
                    data[key] = clean(data[key]);
                });
            }
            return data;
        };

        if (req.body) req.body = clean(req.body);
        if (req.params) req.params = clean(req.params);
        try {
            if (req.query) req.query = clean(req.query);
        } catch (err) { }

        next();
    });

    // 6. Prevent HTTP Parameter Pollution (skipped if causes issues)
    // app.use(hpp());

    Logger.info('Post-processing security middleware applied: Sanitization');
};

module.exports = { setupPreSecurity, setupPostSecurity };
