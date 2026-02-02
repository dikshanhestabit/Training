const express = require('express');
const config = require('./config');
const Logger = require('./utils/logger');
const dbLoader = require('./loaders/db');
const expressLoader = require('./loaders/app');
const { loadRedis } = require('./loaders/redis');
const { initEmailQueue, initEmailWorker } = require('./jobs/email.job');

async function startServer() {
    const app = express();

    await dbLoader();
    await loadRedis();

    initEmailQueue();
    initEmailWorker();

    require('./models/User');
    require('./models/Product');

    await expressLoader({ app });

    app.listen(config.port, () => {
        Logger.info(`Server started on port ${config.port}`);
    }).on('error', err => {
        Logger.error(err);
        process.exit(1);
    });
}

startServer();
