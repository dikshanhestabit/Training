const express = require('express');
const router = express.Router();
const { addEmailJob } = require('../../jobs/email.job');
const Logger = require('../../utils/logger');

router.post('/email', async (req, res, next) => {
    try {
        const { to, subject, body } = req.body;

        if (!to || !subject || !body) {
            return res.status(400).json({ error: 'Missing required fields: to, subject, body' });
        }

        const job = await addEmailJob({ to, subject, body });

        res.status(202).json({
            success: true,
            message: 'Job added to queue',
            jobId: job.id,
        });
    } catch (error) {
        Logger.error('Failed to add job to queue:', error);
        next(error);
    }
});

module.exports = router;
