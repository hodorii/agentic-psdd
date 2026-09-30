# {{label.title_authentication_standards}}

[Purpose: unify auth model, token/session lifecycle, permission checks, and security]

## {{label.philosophy}}
- Clear separation: authentication (who) vs authorization (what)
- Secure by default: least privilege, fail closed, short-lived tokens
- UX-aware: friction where risk is high, smooth otherwise

## {{label.authentication}}

### {{label.auth_method}}
- Options: JWT, Session, OAuth2, hybrid
- Choice: [our method] because [reason]

### {{label.auth_flow}}
```
1) User proves identity (credentials or provider)
2) Server verifies and issues token/session
3) Client sends token per request
4) Server verifies token and proceeds
```

### {{label.token_session_lifecycle}}
- Storage: httpOnly cookie or Authorization header
- Expiration: short-lived access, longer refresh (if used)
- Refresh: rotate tokens; respect revocation
- Revocation: blacklist/rotate on logout/compromise

### {{label.security_pattern}}
- Enforce TLS; never expose tokens to JS when avoidable
- Bind token to audience/issuer; include minimal claims
- Consider device binding and IP/risk checks for sensitive actions

## {{label.authorization}}

### {{label.permission_model}}
- Choose one: RBAC / ABAC / ownership-based / hybrid
- Define roles/attributes centrally; avoid hardcoding across codebase

### {{label.authorization_checks}}
- Route/middleware: coarse-grained gate
- Domain/service: fine-grained decisions
- UI: conditional rendering (no security reliance)

Example pattern:
```typescript
requirePermission('resource:action'); // route
if (!user.can('resource:action')) throw ForbiddenError(); // domain
```

### {{label.ownership}}
- Pattern: owner OR privileged role can act
- Verify on entity boundary before mutation

## {{label.passwords_mfa}}
- Passwords: strong policy, hashed (bcrypt/argon2), never plaintext
- Reset: time-limited token, single-use, notify user
- MFA: step-up for risky operations (policy-driven)

## {{label.api_to_api_auth}}
- Use API keys or OAuth client credentials
- Scope keys minimally; rotate and audit usage
- Rate limit by identity (user/key)

<!-- Focus on patterns and decisions. No library-specific code. -->
