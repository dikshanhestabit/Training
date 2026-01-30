const Joi = require('joi');
const Logger = require('../utils/logger');

// Define generic validation middleware
const validate = (schema) => (req, res, next) => {
    const { error, value } = schema.validate(req.body, { abortEarly: false });
    if (error) {
        const errorMessages = error.details.map((detail) => detail.message).join(', ');
        Logger.warn(`Validation Error: ${errorMessages}`);
        return res.status(400).json({ error: 'Validation Error', details: errorMessages });
    }
    Object.assign(req, value);
    return next();
};

// Define schemas
const schemas = {
    // User Validation Schemas
    user: {
        register: Joi.object({
            firstName: Joi.string().required().trim().min(2).max(30),
            lastName: Joi.string().required().trim().min(2).max(30),
            email: Joi.string().email().required().lowercase(),
            password: Joi.string().min(8).required(), // Add strength requirements if needed
        }),
        login: Joi.object({
            email: Joi.string().email().required().lowercase(),
            password: Joi.string().required(),
        }),
        update: Joi.object({
            firstName: Joi.string().optional().trim().min(2).max(30),
            lastName: Joi.string().optional().trim().min(2).max(30),
            email: Joi.string().email().optional().lowercase(),
            password: Joi.string().min(8).optional(),
            status: Joi.string().valid('active', 'inactive').optional(),
        }).min(1),
    },
    // Product Validation Schemas
    product: {
        create: Joi.object({
            name: Joi.string().required().trim().min(3).max(100),
            price: Joi.number().required().min(0),
            description: Joi.string().optional().trim().max(500),
            category: Joi.string().optional().trim(),
            stock: Joi.number().min(0).default(0),
            tags: Joi.array().items(Joi.string().trim()).default([]),
            status: Joi.string().valid('active', 'inactive').default('active'),
            rating: Joi.number().min(0).max(5).default(0),
        }),
        update: Joi.object({
            name: Joi.string().optional().trim().min(3).max(100),
            price: Joi.number().optional().min(0),
            description: Joi.string().optional().trim().max(500),
            category: Joi.string().optional().trim(),
            stock: Joi.number().optional().min(0),
            tags: Joi.array().items(Joi.string().trim()).optional(),
            status: Joi.string().valid('active', 'inactive').optional(),
            rating: Joi.number().min(0).max(5).optional(),
        }).min(1), // Require at least one field to update
    },
};

module.exports = {
    validate,
    schemas,
};
