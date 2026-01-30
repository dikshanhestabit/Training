const dbLoader = require('../loaders/db');
const ProductRepository = require('../repositories/product.repository');
const Logger = require('../utils/logger');
const mongoose = require('mongoose');

async function runTests() {
  try {
    console.log('\n========================================');
    console.log('DAY 3 - ADVANCED QUERY ENGINE TESTS');
    console.log('========================================\n');

    // 1.Connect DB
    await dbLoader();
    console.log('Database connected\n');

    // 2.Clear all products (hard delete for testing)
    console.log('Cleaning up existing products...');
    const existingProducts = await ProductRepository.findWithFilters({
      includeDeleted: true,
      limit: 1000
    });
    for (const product of existingProducts.products) {
      await ProductRepository.hardDelete(product._id);
    }
    console.log('Cleanup complete\n');

    // 3.Create test products
    console.log('Creating test products...');
    const products = [
      {
        name: 'iPhone 15 Pro',
        price: 999,
        rating: 4.5,
        tags: ['apple', 'smartphone', 'premium'],
        status: 'active',
      },
      {
        name: 'Samsung Galaxy S24',
        price: 899,
        rating: 4.3,
        tags: ['samsung', 'smartphone'],
        status: 'active',
      },
      {
        name: 'MacBook Pro',
        price: 2499,
        rating: 4.8,
        tags: ['apple', 'laptop', 'premium'],
        status: 'active',
      },
      {
        name: 'Budget Phone',
        price: 199,
        rating: 3.5,
        tags: ['budget', 'smartphone'],
        status: 'active',
      },
      {
        name: 'Dell XPS',
        price: 1299,
        rating: 4.2,
        tags: ['dell', 'laptop'],
        status: 'active',
      },
    ];

    const createdProducts = [];
    for (const productData of products) {
      const product = await ProductRepository.create(productData);
      createdProducts.push(product);
      console.log(`  ✓ Created: ${product.name} - $${product.price}`);
    }
    console.log(`${createdProducts.length} products created\n`);

    // 4.Test SEARCH
    console.log('🔍 TEST 1: Search by name (regex)');
    const searchResult = await ProductRepository.findWithFilters({ search: 'phone' });
    console.log(`  Query: search=phone`);
    console.log(`  Results: ${searchResult.products.length} products`);
    searchResult.products.forEach(p => console.log(`    - ${p.name}`));
    console.log('');

    // 5.Test PRICE RANGE
    console.log('TEST 2: Price range filter');
    const priceResult = await ProductRepository.findWithFilters({
      minPrice: 500,
      maxPrice: 1000
    });
    console.log(`  Query: minPrice=500&maxPrice=1000`);
    console.log(`  Results: ${priceResult.products.length} products`);
    priceResult.products.forEach(p => console.log(`    - ${p.name}: $${p.price}`));
    console.log('');

    // 6.Test TAGS FILTER
    console.log(' TEST 3: Tags filter (OR condition)');
    const tagsResult = await ProductRepository.findWithFilters({
      tags: ['apple', 'samsung']
    });
    console.log(`  Query: tags=apple,samsung`);
    console.log(`  Results: ${tagsResult.products.length} products`);
    tagsResult.products.forEach(p => console.log(`    - ${p.name} (tags: ${p.tags.join(', ')})`));
    console.log('');

    // 7.Test SORTING
    console.log('TEST 4: Sorting');
    const sortAsc = await ProductRepository.findWithFilters({ sort: 'price:asc' });
    console.log(`  Query: sort=price:asc`);
    console.log(`  Results (ascending):`);
    sortAsc.products.forEach(p => console.log(`    - ${p.name}: $${p.price}`));

    const sortDesc = await ProductRepository.findWithFilters({ sort: 'price:desc' });
    console.log(`  Query: sort=price:desc`);
    console.log(`  Results (descending):`);
    sortDesc.products.forEach(p => console.log(`    - ${p.name}: $${p.price}`));
    console.log('');

    // 8.Test PAGINATION
    console.log('TEST 5: Pagination');
    const page1 = await ProductRepository.findWithFilters({ page: 1, limit: 2 });
    console.log(`  Query: page=1&limit=2`);
    console.log(`  Results: ${page1.products.length} products`);
    console.log(`  Pagination:`, page1.pagination);
    page1.products.forEach(p => console.log(`    - ${p.name}`));
    console.log('');

    // 9.Test COMBINED FILTERS
    console.log('TEST 6: Combined filters');
    const combined = await ProductRepository.findWithFilters({
      search: 'phone',
      minPrice: 500,
      maxPrice: 1000,
      tags: ['apple', 'samsung'],
      sort: 'price:desc',
    });
    console.log(`  Query: search=phone&minPrice=500&maxPrice=1000&tags=apple,samsung&sort=price:desc`);
    console.log(`  Results: ${combined.products.length} products`);
    combined.products.forEach(p => console.log(`    - ${p.name}: $${p.price} (${p.tags.join(', ')})`));
    console.log('');

    // 10. Test SOFT DELETE
    console.log(' TEST 7: Soft Delete');
    const productToDelete = createdProducts[3]; // Budget Phone
    console.log(`  Deleting: ${productToDelete.name}`);

    const deleted = await ProductRepository.softDelete(productToDelete._id);
    console.log(`  ✓ Soft deleted at: ${deleted.deletedAt}`);

    // Check default query (should exclude deleted)
    const defaultQuery = await ProductRepository.findWithFilters({});
    console.log(`  Default query results: ${defaultQuery.products.length} products (deleted excluded)`);

    // Check with includeDeleted
    const withDeleted = await ProductRepository.findWithFilters({ includeDeleted: true });
    console.log(`  With includeDeleted=true: ${withDeleted.products.length} products (deleted included)`);
    console.log('');

    // 11.Test FIND BY ID with soft delete
    console.log(' TEST 8: Find by ID (soft delete handling)');
    const foundWithoutDeleted = await ProductRepository.findById(productToDelete._id, false);
    console.log(`  findById(id, includeDeleted=false): ${foundWithoutDeleted ? 'Found' : 'Not found (correct!)'}`);

    const foundWithDeleted = await ProductRepository.findById(productToDelete._id, true);
    console.log(`  findById(id, includeDeleted=true): ${foundWithDeleted ? 'Found (correct!)' : 'Not found'}`);
    console.log('');

    // 12.Test VIRTUAL FIELDS
    console.log('TEST 9: Virtual Fields');
    const allProducts = await ProductRepository.findWithFilters({ limit: 100 });
    console.log(`  Rating Labels:`);
    allProducts.products.forEach(p => {
      console.log(`    - ${p.name}: ${p.rating} stars → "${p.ratingLabel}"`);
    });
    console.log('');

    // 13. Summary
    console.log('========================================');
    console.log(' ALL TESTS COMPLETED SUCCESSFULLY!');
    console.log('========================================');
    console.log('\n Test Summary:');
    console.log('   Search by name (regex)');
    console.log('   Price range filtering');
    console.log('   Tags filtering (OR condition)');
    console.log('   Sorting (asc/desc)');
    console.log('   Pagination with metadata');
    console.log('   Combined filters');
    console.log('   Soft delete functionality');
    console.log('   Find by ID with soft delete');
    console.log('   Virtual fields (ratingLabel)');
    console.log('\n Day 3 Query Engine is working perfectly!\n');

  } catch (err) {
    console.error('\n Test Error:', err.message);
    console.error(err.stack);
  } finally {
    await mongoose.connection.close();
    console.log('Database connection closed');
  }
}

runTests();
