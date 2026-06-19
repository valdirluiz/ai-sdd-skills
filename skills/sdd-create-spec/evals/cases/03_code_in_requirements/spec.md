# Two-Factor Authentication

## Overview

Users need a second authentication factor to improve account security beyond passwords alone.

## Problem Statement

Accounts secured only by passwords are vulnerable to credential stuffing and phishing. Enterprise customers require two-factor authentication for compliance purposes.

## Goals

- Protect user accounts against unauthorized access
- Meet enterprise compliance requirements for authentication

## Non-Goals

- Hardware security key support (FIDO2/WebAuthn)
- Biometric authentication

## Requirements

### Functional Requirements

- **FR-01**: Users must be able to enroll a TOTP authenticator app as a second factor
- **FR-02**: After enrolling, users must provide a TOTP code on each login
- **FR-03**: Users must be provided with backup codes at enrollment time

Here is how the enrollment endpoint should work:

```json
POST /api/auth/totp/enroll
{
  "user_id": "uuid",
  "secret": "BASE32_ENCODED_SECRET"
}
```

### Non-Functional Requirements

- **NFR-01**: Security — TOTP codes must be single-use and expire after 30 seconds
- **NFR-02**: Security — backup codes must be hashed before storage using bcrypt

## User Stories

- **US-01**: As a security-conscious user, I want to enable two-factor authentication, so that my account is protected even if my password is compromised.
- **US-02**: As an enterprise admin, I want to require 2FA for all users in my organization, so that we meet our security compliance requirements.

## Acceptance Criteria

- [ ] **AC-01**: Given an unenrolled user, When they navigate to security settings, Then they see an option to enable 2FA
- [ ] **AC-02**: Given an enrolled user, When they log in with correct credentials, Then they are prompted for a TOTP code before access is granted
- [ ] **AC-03**: Given a valid TOTP code, When submitted during login, Then the user gains access to their account

## Open Questions

1. Should admins be able to bypass 2FA for individual users in emergency situations?
