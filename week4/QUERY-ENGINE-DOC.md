# Product Query Engine Documentation

## Overview

This document describes the advanced query engine for the Product API, which supports dynamic filtering, searching, sorting, pagination, and soft delete functionality.


## Base Endpoint

```
GET /api/products
```


## Supported Query Parameters

### Search

Search products by name using case-insensitive regex.

```
?search=phone
```

- Matches partial words  
- Case-insensitive  

### Price Range Filter

Filter products within a price range.

```
?minPrice=500&maxPrice=1000
```

- `minPrice` → minimum price (inclusive)
- `maxPrice` → maximum price (inclusive)


### Tags Filter (OR condition)

Filter products that match **any** of the provided tags.

```
?tags=apple,samsung
```

- Matches products containing **at least one** tag  
- Comma-separated values  


### Sorting

Sort results by any field.

```
?sort=price:asc
?sort=price:desc
```

Format:
```
sort=field:order
```

- `asc` → ascending
- `desc` → descending

Default sorting:
```
createdAt:desc
```


### Pagination

Paginate large result sets.

```
?page=1&limit=10
```

- `page` → page number (default: 1)
- `limit` → items per page (default: 10)

Response includes pagination metadata:
- current page
- total items
- total pages


### Soft Delete Handling

By default, **soft-deleted products are excluded**.

Include them explicitly:

```
?includeDeleted=true
```


## Combined Queries

Multiple filters can be combined in a single request.

Example:

```
?search=phone
&minPrice=500
&maxPrice=1000
&tags=apple,samsung
&sort=price:desc
&page=1
&limit=5
```


## Default Behavior Summary

| Feature | Default |
|------|--------|
| Sorting | `createdAt:desc` |
| Pagination | page=1, limit=10 |
| Soft-deleted records | Excluded |
| Tag matching | OR condition |


## Error Responses (High Level)

All errors follow a consistent format:

- Invalid input → `400`
- Not found → `404`
- Server error → `500`

Each error includes:
- message
- error code
- timestamp
- request path



