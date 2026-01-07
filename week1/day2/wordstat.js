#!/usr/bin/env node

const startTime = process.hrtime.bigint();
const startMemory = process.memoryUsage().heapUsed;


const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);

// Parse CLI args
const options = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith("--")) {
    const key = args[i].replace("--", "");
    const value =
      args[i + 1] && !args[i + 1].startsWith("--")
        ? args[++i]
        : true;
    options[key] = value;
  }
}

// Validate file option
if (!options.file) {
  console.error("Error: --file argument is required");
  process.exit(1);
}

const filePath = path.resolve(options.file);

if (!fs.existsSync(filePath)) {
  console.error(`Error: File not found -> ${filePath}`);
  process.exit(1);
}

// Read file
const content = fs.readFileSync(filePath, "utf8");

console.log("File read successfully");
console.log("File size (bytes):", Buffer.byteLength(content));

// Word processing
const minLen = options.minLen ? parseInt(options.minLen) : 1;
const topN = options.top ? parseInt(options.top) : 10;
const concurrency = options.concurrency
  ? parseInt(options.concurrency)
  : 1;

// Normalize and split words
const allWords = content
  .toLowerCase()
  .replace(/[^a-z0-9\s]/g, "")
  .split(/\s+/)
  .filter(w => w.length >= minLen && w.length > 0);

// Split words into chunks
function chunkArray(arr, chunks) {
  const size = Math.ceil(arr.length / chunks);
  const result = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

// Process a chunk
function processChunk(words) {
  return new Promise(resolve => {
    const freq = {};
    for (const word of words) {
      freq[word] = (freq[word] || 0) + 1;
    }
    resolve(freq);
  });
}
// Run concurrent processing
(async () => {
  const chunks = chunkArray(allWords, concurrency);

  const results = await Promise.all(
    chunks.map(chunk => processChunk(chunk))
  );

  // Merge frequencies
  const finalFreq = {};
  for (const result of results) {
    for (const word in result) {
      finalFreq[word] = (finalFreq[word] || 0) + result[word];
    }
  }

  const totalWords = allWords.length;
  const uniqueWordsCount = Object.keys(finalFreq).length;

  let longestWord = "";
  let shortestWord = allWords[0] || "";

  for (const word of allWords) {
    if (word.length > longestWord.length) longestWord = word;
    if (word.length < shortestWord.length) shortestWord = word;
  }

  const topWords = Object.entries(finalFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, count]) => ({ word, count }));

  console.log("Concurrency level:", concurrency);
  console.log("Total words:", totalWords);

  if (options.unique) {
    console.log("Unique words:", uniqueWordsCount);
  }

  console.log("Longest word:", longestWord);
  console.log("Shortest word:", shortestWord);
  console.table(topWords);
  
const stats = {
  file: options.file,
  concurrency,
  totalWords,
  uniqueWords: options.unique ? uniqueWordsCount : undefined,
  longestWord,
  shortestWord,
  topWords
};

const outputPath = path.join("output", "stats.json");
fs.writeFileSync(outputPath, JSON.stringify(stats, null, 2));


  const endTime = process.hrtime.bigint();
  const endMemory = process.memoryUsage().heapUsed;

  const executionTimeMs = Number(endTime - startTime) / 1_000_000;
  const memoryUsedMB = (endMemory - startMemory) / (1024 * 1024);

  const perfResult = {
    concurrency,
    executionTimeMs: executionTimeMs.toFixed(2),
    memoryUsedMB: memoryUsedMB.toFixed(2)
  };

  const logPath = path.join("logs", "perf-summary.json");

  let existing = [];
  if (fs.existsSync(logPath)) {
    existing = JSON.parse(fs.readFileSync(logPath, "utf8"));
  }

  existing.push(perfResult);
  fs.writeFileSync(logPath, JSON.stringify(existing, null, 2));


})();


