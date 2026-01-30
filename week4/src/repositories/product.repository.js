const Product = require('../models/Product');

class ProductRepository {
  /**
   * Create a new product
   */
  async create(data) {
    return Product.create(data);
  }

  /**
   * Find product by ID
   */
  async findById(id, includeDeleted = false) {
    const query = { _id: id };
    if (!includeDeleted) {
      query.deletedAt = null;
    }
    return Product.findOne(query);
  }

  /**
   * Advanced query with filters, search, sort, pagination
   */
  async findWithFilters({
    search = '',
    minPrice,
    maxPrice,
    tags = [],
    sort = 'createdAt:desc',
    page = 1,
    limit = 10,
    includeDeleted = false,
  }) {
    // Build query object
    const query = {};

    // Soft delete filter
    if (!includeDeleted) {
      query.deletedAt = null;
    }

    // Search by name (regex, case-insensitive)
    if (search) {
      query.name = { $regex: search, $options: 'i' };
    }

    // Price range filter
    if (minPrice !== undefined || maxPrice !== undefined) {
      query.price = {};
      if (minPrice !== undefined) query.price.$gte = Number(minPrice);
      if (maxPrice !== undefined) query.price.$lte = Number(maxPrice);
    }

    // Tags filter (OR condition - match any tag)
    if (tags.length > 0) {
      query.tags = { $in: tags };
    }

    // Parse sort parameter (e.g., "price:desc" or "rating:asc")
    const [sortField, sortOrder] = sort.split(':');
    const sortObj = { [sortField]: sortOrder === 'asc' ? 1 : -1 };

    // Pagination
    const skip = (page - 1) * limit;

    // Execute query
    const products = await Product.find(query)
      .sort(sortObj)
      .skip(skip)
      .limit(Number(limit));

    // Get total count for pagination
    const total = await Product.countDocuments(query);

    return {
      products,
      pagination: {
        page: Number(page),
        limit: Number(limit),
        total,
        pages: Math.ceil(total / limit),
      },
    };
  }

  /**
   * Update product by ID
   */
  async update(id, data) {
    return Product.findByIdAndUpdate(id, data, { new: true, runValidators: true });
  }

  /**
   * Soft delete - set deletedAt timestamp
   */
  async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }

  /**
   * Hard delete (for cleanup/testing)
   */
  async hardDelete(id) {
    return Product.findByIdAndDelete(id);
  }
}

module.exports = new ProductRepository();
