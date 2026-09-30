# {{label.title_security_standards}}

[Purpose: define security posture with patterns for validation, authz, secrets, and data]

## {{label.philosophy}}
- Defense in depth; least privilege; secure by default; fail closed
- Validate at boundaries; sanitize for context; never trust input
- Separate authentication (who) and authorization (what)

## {{label.input_output}}
- Validate at API boundaries and UI forms; enforce types and constraints
- Sanitize/escape based on destination (HTML, SQL, shell, logs)
- Prefer allow-lists over block-lists; reject early with minimal detail

## {{label.authentication_authorization}}
- Authentication: verify identity; issue short-lived tokens/sessions
- Authorization: check permissions before actions; deny by default
- Centralize policies; avoid duplicating checks across code

Pattern:
```typescript
if (!user.hasPermission('resource:action')) throw ForbiddenError();
```

## {{label.secrets_configuration}}
- Never commit secrets; store in secret manager or env
- Rotate regularly; audit access; scope minimal
- Validate required env vars at startup; fail fast on missing

## {{label.sensitive_data}}
- Minimize collection; mask/redact in logs; encrypt at rest and in transit
- Restrict access by role/need-to-know; track access to sensitive records

## {{label.session_token_security}}
- httpOnly + secure cookies where possible; TLS everywhere
- Short expiration; rotate on refresh; revoke on logout/compromise
- Bind tokens to audience/issuer; include minimal claims

## {{label.security_logging}}
- Log auth attempts, permission denials, and sensitive operations
- Never log passwords, tokens, secrets, full PII; avoid full bodies
- Include requestId and context to correlate events

## {{label.headers_transport}}
- Enforce TLS; HSTS
- Set security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Prefer modern crypto; disable weak protocols/ciphers

## {{label.vulnerability_posture}}
- Prefer secure libraries; keep dependencies updated
- Static/dynamic scans in CI; track and remediate
- Educate team on common classes; encode as patterns above

<!-- Focus on patterns and principles. Link concrete configs to ops docs. -->
