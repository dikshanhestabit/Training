const express = require('express');
const router = express.Router();

const healthRoutes = require('./api/health');
const userRoutes = require('./api/users');

router.use('/health', healthRoutes);
router.use('/users', userRoutes);

module.exports = router;
