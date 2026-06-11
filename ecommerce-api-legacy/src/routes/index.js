const express = require('express');
const checkoutController = require('../controllers/checkoutController');
const courseController = require('../controllers/courseController');
const userController = require('../controllers/userController');

const router = express.Router();

// Health check
router.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'ecommerce-api-legacy' });
});

// Checkout
router.post('/api/checkout', (req, res, next) => checkoutController.checkout(req, res, next));

// Financial report
router.get('/api/admin/financial-report', (req, res, next) => courseController.getFinancialReport(req, res, next));

// Users
router.delete('/api/users/:id', (req, res, next) => userController.deleteUser(req, res, next));

module.exports = router;
