const dbLoader = require('../loaders/db');
const UserRepository = require('../repositories/user.repository');
const ProductRepository = require('../repositories/product.repository');
const Logger = require('../utils/logger');
const mongoose = require('mongoose');
const User = require('../models/User');
const Product = require('../models/Product');

async function runTests() {
  try {
    console.log('--- DAY 2 REPOSITORY TESTS START ---');

    // 1️⃣ Connect DB
    await dbLoader();

    // 2️⃣ Clear collections using repository methods
    // Fetch all users and delete them
    const allUsers = await UserRepository.findPaginated({ page: 1, limit: 1000 });
    for (const user of allUsers.data) {
      await UserRepository.delete(user._id);
    }

    // Fetch all products and delete them
    const allProducts = await ProductRepository.findPaginated({ page: 1, limit: 1000 });
    for (const product of allProducts) {
      await ProductRepository.delete(product._id);
    }

    // 3️⃣ Test CREATE
    const user = await UserRepository.create({
      firstName: 'Dia',
      lastName: 'Sharma',
      email: 'dia@example.com',
      password: 'Password123!',
      status: 'active',
    });

    const product = await ProductRepository.create({
      name: 'Laptop',
      price: 90000,
      rating: 4.5,
      status: 'active',
    });


    console.log('User Created:', {
      id: user._id,
      fullName: user.fullName,
      email: user.email,
    });

    const userWithPassword = await User.findById(user._id).select('+password');
    console.log('Hashed password:', userWithPassword.password);

    console.log('Product Created:', {
      id: product._id,
      name: product.name,
      rating: product.rating,
      ratingLabel: product.ratingLabel,
    });

    // 4️⃣ Test FIND BY ID
    const foundUser = await UserRepository.findById(user._id);
    const foundProduct = await ProductRepository.findById(product._id);

    console.log('Found User by ID:', foundUser.fullName);
    console.log('Found Product by ID:', foundProduct.name);

    // 5️⃣ Test PAGINATION
    const usersPage = await UserRepository.findPaginated({ page: 1, limit: 10 });
    const productsPage = await ProductRepository.findPaginated({ page: 1, limit: 10 });

    console.log('Users Page 1:', usersPage.data.length, 'records');
    console.log('Products Page 1:', productsPage.length, 'records');

    // 6️⃣ Test UPDATE
    await UserRepository.update(user._id, { status: 'inactive' });
    await ProductRepository.update(product._id, { price: 1000 });

    const updatedUser = await UserRepository.findById(user._id);
    const updatedProduct = await ProductRepository.findById(product._id);

    console.log('Updated User Status:', updatedUser.status);
    console.log('Updated Product Price:', updatedProduct.price);

    // 7️⃣ Test DELETE
    await UserRepository.delete(user._id);
    await ProductRepository.delete(product._id);

    const checkUser = await UserRepository.findById(user._id);
    const checkProduct = await ProductRepository.findById(product._id);

    console.log('User after delete:', checkUser); // should be null
    console.log('Product after delete:', checkProduct); // should be null

    console.log('--- DAY 2 REPOSITORY TESTS END ---');

  } catch (err) {
    console.error('Test Error:', err);
  } finally {
    await mongoose.connection.close();
  }
}

runTests();
