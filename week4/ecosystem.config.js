module.exports = {
    apps: [
        {
            name: 'week4-api',
            script: 'src/index.js',
            instances: 'max',
            exec_mode: 'cluster',
            env: {
                NODE_ENV: 'production',
                PORT: 3000,
            },
            env_development: {
                NODE_ENV: 'development',
                PORT: 3001,
            },
            log_date_format: 'YYYY-MM-DD HH:mm:ss',
            combine_logs: true,
            error_file: 'logs/err.log',
            out_file: 'logs/out.log',
        },
    ],
};
