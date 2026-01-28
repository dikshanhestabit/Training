const dotenv = require('dotenv');
const path = require('path');

// Set the NODE_ENV to 'development' by default
process.env.NODE_ENV = process.env.NODE_ENV || 'development';

const envFound = dotenv.config({
    path: path.resolve(__dirname, `../../.env.${process.env.NODE_ENV === 'development' ? 'dev' : process.env.NODE_ENV}`),
});

// Fallback to .env.local if specific env file is not found
if (envFound.error) {
    dotenv.config({ path: path.resolve(__dirname, '../../.env.local') });
}

module.exports = {
    port: parseInt(process.env.PORT, 10) || 3000,
    databaseURL: process.env.MONGODB_URI,
    logs: {
        level: process.env.LOG_LEVEL || 'silly',
    },
    api: {
        prefix: '/api',
    },
};
