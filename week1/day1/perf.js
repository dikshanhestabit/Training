const fs = require('fs');
const path = require('path');

const FILE_PATH = path.join(__dirname, 'data', 'large-file.txt');

function formatMB(bytes) {
  return (bytes / 1024 / 1024).toFixed(2);
}

async function bufferRead() {
  const startMem = process.memoryUsage().rss;
  const start = process.hrtime.bigint();

  fs.readFileSync(FILE_PATH);

  const end = process.hrtime.bigint();
  const endMem = process.memoryUsage().rss;

  return {
    method: 'buffer',
    executionTimeMs: Number(end - start) / 1e6,
    memoryUsedMB: formatMB(endMem - startMem),
  };
}

async function streamRead() {
  const startMem = process.memoryUsage().rss;
  const start = process.hrtime.bigint();

  return new Promise((resolve) => {
    const stream = fs.createReadStream(FILE_PATH);
    stream.on('data', () => {});
    stream.on('end', () => {
      const end = process.hrtime.bigint();
      const endMem = process.memoryUsage().rss;

      resolve({
        method: 'stream',
        executionTimeMs: Number(end - start) / 1e6,
        memoryUsedMB: formatMB(endMem - startMem),
      });
    });
  });
}

(async () => {
  const bufferResult = await bufferRead();
  const streamResult = await streamRead();

  const result = {
    timestamp: new Date().toISOString(),
    fileSizeMB: 100,
    results: [bufferResult, streamResult],
  };

  fs.mkdirSync('logs', { recursive: true });
  fs.writeFileSync(
    'logs/day1-perf.json',
    JSON.stringify(result, null, 2)
  );

  console.log('Performance benchmark completed.');
})();
