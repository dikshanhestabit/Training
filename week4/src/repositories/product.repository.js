const Product = require('../models/Product');

class ProductRepository {
  async create(data) {
    return Product.create(data);
  }

  async findById(id) {
    return Product.findById(id);
  }

  async findPaginated({ page = 1, limit = 10 }) {
    const skip = (page - 1) * limit;

    return Product.find()
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit);
  }

  async update(id, data) {
    return Product.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return Product.findByIdAndDelete(id);
  }
}

module.exports = new ProductRepository();
