const express = require('express');
const router = express.Router();
const productController = require('../../controllers/product.controller');
const { validate, schemas } = require('../../middlewares/validate');

/**
 * Product Routes
 */
router.get('/', productController.getProducts);
router.get('/:id', productController.getProductById);
router.post('/', validate(schemas.product.create), productController.createProduct);
router.put('/:id', validate(schemas.product.update), productController.updateProduct);
router.delete('/:id', productController.deleteProduct);

module.exports = router;
