const productService = require('../services/product.service');

/**
 * Get all products with filters
 * GET /products?search=phone&minPrice=100&maxPrice=500&sort=price:desc&tags=apple,samsung&page=1&limit=10&includeDeleted=false
 */
exports.getProducts = async (req, res, next) => {
    try {
        const result = await productService.getProducts(req.query);

        res.status(200).json({
            success: true,
            data: result.products,
            pagination: result.pagination,
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Get single product by ID
 * GET /products/:id
 */
exports.getProductById = async (req, res, next) => {
    try {
        const { id } = req.params;
        const includeDeleted = req.query.includeDeleted === 'true';

        const product = await productService.getProductById(id, includeDeleted);

        res.status(200).json({
            success: true,
            data: product,
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Create new product
 * POST /products
 */
exports.createProduct = async (req, res, next) => {
    try {
        const product = await productService.createProduct(req.body);

        res.status(201).json({
            success: true,
            message: 'Product created successfully',
            data: product,
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Update product
 * PUT /products/:id
 */
exports.updateProduct = async (req, res, next) => {
    try {
        const { id } = req.params;
        const product = await productService.updateProduct(id, req.body);

        res.status(200).json({
            success: true,
            message: 'Product updated successfully',
            data: product,
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Soft delete product
 * DELETE /products/:id
 */
exports.deleteProduct = async (req, res, next) => {
    try {
        const { id } = req.params;
        const product = await productService.deleteProduct(id);

        res.status(200).json({
            success: true,
            message: 'Product deleted successfully',
            data: product,
        });
    } catch (error) {
        next(error);
    }
};
