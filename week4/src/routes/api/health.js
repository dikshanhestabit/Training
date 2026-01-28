const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date() });
});

router.get('/db', (req, res) => {
    res.json({ database: 'connected' });
});

module.exports = router;
