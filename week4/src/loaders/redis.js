const Redis = require('ioredis');
const RedisMock = require('ioredis-mock');
const Logger = require('../utils/logger');
const config = require('../config');

let redisClient;

const loadRedis = async () => {
    try {
        const useMock = process.env.REDIS_USE_MOCK === 'true';

        if (useMock) {
            Logger.info('Using ioredis-mock for background jobs (In-memory)');
            redisClient = new RedisMock({
                // BullMQ requires some specific behaviors that mock might struggle with
                data_storage_mode: 'in-memory'
            });
        } else {
            redisClient = new Redis({
                host: process.env.REDIS_HOST || '127.0.0.1',
                port: process.env.REDIS_PORT || 6379,
                maxRetriesPerRequest: null,
            });

            redisClient.on('error', (err) => {
                Logger.error('Redis connection error. If Redis is not installed, set REDIS_USE_MOCK=true in .env');
            });
        }

        return redisClient;
    } catch (error) {
        Logger.error('Failed to initialize Redis:', error);
        throw error;
    }
};

const getRedisClient = () => {
    if (!redisClient) {
        throw new Error('Redis client not initialized. Call loadRedis first.');
    }
    return redisClient;
};

module.exports = {
    loadRedis,
    getRedisClient,
};
