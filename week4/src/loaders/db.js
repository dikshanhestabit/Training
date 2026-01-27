const mongoose = require('mongoose');
const config = require('../config');
const Logger = require('../utils/logger');

module.exports = async () => {
    try {
        const connection = await mongoose.connect(config.databaseURL);
        Logger.info('Database connected');
        return connection.connection.db;
    } catch (err) {
        Logger.error('🔥 Error connecting to database: %o', err);
        throw err;
    }
};
