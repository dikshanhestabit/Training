# DAY 4 —  HTTP / API FORENSICS (USING CURL + POSTMAN + HEADERS)

## Overview
This exercise focuses on understanding how HTTP APIs behave at a low level by inspecting requests, responses, headers, pagination, and caching mechanisms using **cURL** and **Postman**.

## Learning Outcomes

- **HTTP Headers**
  - Inspect request and response headers
  - Modify headers such as `User-Agent`, `Authorization`, and `If-None-Match`
  - Observe server behavior with altered or missing headers

- **Pagination**
  - Understand offset-based pagination using query parameters
  - Analyze `limit` and `skip` in API responses

- **ETag Caching**
  - Capture `ETag` values from server responses
  - Perform conditional requests using `If-None-Match`
  - Interpret `304 Not Modified` responses

- **Request–Response Cycle**
  - Trace full HTTP request–response flow
  - Compare behavior across cURL and Postman
  - Validate caching and header handling using a custom Node.js server
    
## Tools Used
- cURL (command-line HTTP client)
- Postman Desktop Agent
- Node.js (for local HTTP server)

