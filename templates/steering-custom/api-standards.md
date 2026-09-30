# {{label.title_api_standards}}

[Purpose: consistent API patterns for naming, structure, auth, versioning, and errors]

## {{label.philosophy}}
- Prefer predictable, resource-oriented design
- Be explicit in contracts; minimize breaking changes
- Secure by default (auth first, least privilege)

## {{label.endpoint_pattern}}
```
/{version}/{resource}[/{id}][/{sub-resource}]
```
Examples:
- `/api/v1/users`
- `/api/v1/users/:id`
- `/api/v1/users/:id/posts`

HTTP verbs:
- GET (read, safe, idempotent)
- POST (create)
- PUT/PATCH (update)
- DELETE (remove, idempotent)

## {{label.request_response}}

Request (typical):
```json
{ "data": { ... }, "metadata": { "requestId": "..." } }
```

Success:
```json
{ "data": { ... }, "meta": { "timestamp": "...", "version": "..." } }
```

Error:
```json
{ "error": { "code": "ERROR_CODE", "message": "...", "field": "optional" } }
```
(See error-handling for rules.)

## {{label.status_codes_pattern}}
- 2xx: Success (200 read, 201 create, 204 delete)
- 4xx: Client issues (400 validation, 401/403 auth, 404 missing)
- 5xx: Server issues (500 generic, 503 unavailable)
Choose the status that best reflects the outcome.

## {{label.authentication}}
- Credentials in standard location
```
Authorization: Bearer {token}
```
- Reject unauthenticated before business logic

## {{label.versioning}}
- Version via URL/header/media-type
- Breaking change → new version
- Non-breaking → same version
- Provide deprecation window and comms

## {{label.pagination_filtering}}
- Pagination: `page`, `pageSize` or cursor-based
- Filtering: explicit query params
- Sorting: `sort=field:asc|desc`
Return pagination metadata in `meta`.

---
_Focus on patterns and decisions, not endpoint catalogs._
