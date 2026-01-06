const os = require('os');
const { execSync } = require('child_process');

console.log(`OS: ${os.platform()} ${os.release()}`);
console.log(`Architecture: ${os.arch()}`);
console.log(`CPU Cores: ${os.cpus().length}`);
console.log(`Total Memory: ${(os.totalmem() / 1024 / 1024).toFixed(2)} MB`);
console.log(`System Uptime: ${(os.uptime() / 60).toFixed(2)} minutes`);
console.log(`Current Logged User: ${os.userInfo().username}`);

try {
  const nodePath = execSync('which node').toString().trim();
  console.log(`Node Path: ${nodePath}`);
} catch (error) {
  console.log('Node Path: Not found');
}
