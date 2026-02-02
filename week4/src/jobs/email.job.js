const { Queue, Worker, QueueEvents } = require('bullmq');
const { getRedisClient } = require('../loaders/redis');
const Logger = require('../utils/logger');

const QUEUE_NAME = 'email-notifications';

// 1. Initialize Queue
let emailQueue;

const initEmailQueue = () => {
    const connection = getRedisClient();

    emailQueue = new Queue(QUEUE_NAME, {
        connection,
        defaultJobOptions: {
            attempts: 3,
            backoff: {
                type: 'exponential',
                delay: 1000,
            },
            removeOnComplete: true,
            removeOnFail: false,
        },
    });

    Logger.info(`Job Queue [${QUEUE_NAME}] initialized`);
    return emailQueue;
};

// 2. Define Worker Logic
const initEmailWorker = () => {
    const connection = getRedisClient();

    const worker = new Worker(
        QUEUE_NAME,
        async (job) => {
            const { to, subject, body } = job.data;

            Logger.info(`[Worker] Processing email job ${job.id} for ${to}`);

            // Simulate email sending delay
            await new Promise((resolve) => setTimeout(resolve, 2000));

            // Simulate occasional failure for retry testing
            if (Math.random() < 0.2) {
                throw new Error('Simulated transient email service failure');
            }

            Logger.info(`[Worker] Email sent to ${to}: ${subject}`);
            return { sent: true, recipient: to };
        },
        {
            connection,
            concurrency: 5
        }
    );

    worker.on('completed', (job, returnvalue) => {
        Logger.info(`[Worker] Job ${job.id} completed. Result: ${JSON.stringify(returnvalue)}`);
    });

    worker.on('failed', (job, err) => {
        Logger.error(`[Worker] Job ${job.id} failed after ${job.attemptsMade} attempts. Error: ${err.message}`);
    });

    Logger.info(`Worker for [${QUEUE_NAME}] started`);
    return worker;
};

// 3. Helper to add jobs
const addEmailJob = async (emailData) => {
    if (process.env.REDIS_USE_MOCK === 'true') {
        Logger.info(`[MockQueue] Simulating job entry for ${emailData.to}`);
        // Simulate async processing
        setImmediate(async () => {
            try {
                Logger.info(`[MockWorker] Processing email job for ${emailData.to}`);
                await new Promise(r => setTimeout(r, 1000));
                Logger.info(`[MockWorker] Email sent to ${emailData.to}`);
            } catch (err) {
                Logger.error(`[MockWorker] Job failed: ${err.message}`);
            }
        });
        return { id: `mock-${Date.now()}` };
    }

    if (!emailQueue) {
        throw new Error('Email queue not initialized');
    }
    const job = await emailQueue.add('send-email', emailData);
    Logger.info(`Job ${job.id} added to ${QUEUE_NAME}`);
    return job;
};

module.exports = {
    initEmailQueue: () => {
        if (process.env.REDIS_USE_MOCK === 'true') return null;
        return initEmailQueue();
    },
    initEmailWorker: () => {
        if (process.env.REDIS_USE_MOCK === 'true') return null;
        return initEmailWorker();
    },
    addEmailJob,
};
