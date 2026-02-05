const express = require('express');
const os = require('os');
const app = express();
const PORT = 3000;

app.get('/api', (req, res) => {
    res.json({
        message: "Hello from the Backend!",
        hostname: os.hostname(),
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Backend service listening on port ${PORT}`);
    console.log(`Container Hostname: ${os.hostname()}`);
});
