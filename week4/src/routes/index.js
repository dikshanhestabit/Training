const express = require('express');
const router = express.Router();

const healthRoutes = require('./api/health');
const userRoutes = require('./api/users');
const productRoutes = require('./api/products');
const jobRoutes = require('./api/jobs');

router.use('/health', healthRoutes);
router.use('/users', userRoutes);
router.use('/products', productRoutes);
router.use('/jobs', jobRoutes);

module.exports = router;
