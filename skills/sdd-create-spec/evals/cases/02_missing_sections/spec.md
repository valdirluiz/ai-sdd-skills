# Password Reset

## Overview

Users need a way to recover access to their account when they forget their password.

## Problem Statement

Currently, users who forget their password must contact support to regain access, which creates a high support burden and poor user experience.

## Goals

- Allow users to independently recover account access
- Reduce password-related support tickets

## Requirements

### Functional Requirements

- **FR-01**: Users must be able to initiate a password reset using their registered email address
- **FR-02**: Users must receive a time-limited recovery link
- **FR-03**: Users must be able to set a new password using the recovery link

### Non-Functional Requirements

- **NFR-01**: Security — recovery links must expire after 1 hour
- **NFR-02**: Security — used recovery links must be invalidated immediately

## Acceptance Criteria

- [ ] **AC-01**: Given a user with a registered email, When they request a password reset, Then they receive a recovery email within 5 minutes
- [ ] **AC-02**: Given a valid recovery link, When the user sets a new password, Then they are logged in with the new credentials
- [ ] **AC-03**: Given an expired recovery link, When the user clicks it, Then they are shown an error and prompted to request a new one

## Open Questions

1. Should password reset invalidate all active sessions?
