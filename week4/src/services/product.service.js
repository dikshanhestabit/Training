const productRepository = require('../repositories/product.repository');

class ProductService {
    /**
     * Create a new product
     */
    async createProduct(data) {
        // Validate required fields
        if (!data.name || !data.price) {
            throw new Error('Name and price are required');
        }

        // Validate price
        if (data.price < 0) {
            throw new Error('Price must be a positive number');
        }

        return productRepository.create(data);
    }

    /**
     * Get products with advanced filtering
     */
    async getProducts(queryParams) {
        const {
            search,
            minPrice,
            maxPrice,
            tags,
            sort = 'createdAt:desc',
            page = 1,
            limit = 10,
            includeDeleted = 'false',
        } = queryParams;

        // Parse tags (comma-separated string to array)
        const tagsArray = tags ? tags.split(',').map(tag => tag.trim()) : [];

        // Parse includeDeleted (string to boolean)
        const includeDeletedBool = includeDeleted === 'true';

        const filters = {
            search,
            minPrice,
            maxPrice,
            tags: tagsArray,
            sort,
            page: Number(page),
            limit: Number(limit),
            includeDeleted: includeDeletedBool,
        };

        return productRepository.findWithFilters(filters);
    }

    /**
     * Get single product by ID
     */
    async getProductById(id, includeDeleted = false) {
        const product = await productRepository.findById(id, includeDeleted);

        if (!product) {
            const error = new Error('Product not found');
            error.statusCode = 404;
            error.code = 'PRODUCT_NOT_FOUND';
            throw error;
        }

        return product;
    }

    /**
     * Update product
     */
    async updateProduct(id, data) {
        // Check if product exists
        await this.getProductById(id);

        // Validate price if provided
        if (data.price !== undefined && data.price < 0) {
            throw new Error('Price must be a positive number');
        }

        const updatedProduct = await productRepository.update(id, data);

        if (!updatedProduct) {
            const error = new Error('Failed to update product');
            error.statusCode = 500;
            error.code = 'UPDATE_FAILED';
            throw error;
        }

        return updatedProduct;
    }

    /**
     * Soft delete product
     */
    async deleteProduct(id) {
        // Check if product exists and not already deleted
        const product = await this.getProductById(id);

        if (product.deletedAt) {
            const error = new Error('Product already deleted');
            error.statusCode = 400;
            error.code = 'ALREADY_DELETED';
            throw error;
        }

        return productRepository.softDelete(id);
    }
}

module.exports = new ProductService();
