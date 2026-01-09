const http = require("http");
const url = require("url");

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;


  if (path === "/echo") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(req.headers, null, 2));
  }


  else if (path === "/slow") {
    const delay = parseInt(parsedUrl.query.ms) || 1000;

    setTimeout(() => {
      res.writeHead(200, { "Content-Type": "text/plain" });
      res.end(`Response delayed by ${delay} ms`);
    }, delay);
  }


  else if (path === "/cache") {
    res.writeHead(200, {
      "Content-Type": "text/plain",
      "Cache-Control": "public, max-age=60",
      "ETag": "node-cache-v1"
    });
    res.end("This response is cacheable");
  }


  else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
