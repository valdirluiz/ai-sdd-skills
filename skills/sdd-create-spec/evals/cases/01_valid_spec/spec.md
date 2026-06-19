# Email Notification Preferences

## Overview

Users need control over which email notifications they receive from the platform. Without this feature, users receive all notifications by default and must unsubscribe entirely to reduce noise, leading to account churn and support requests.

## Problem Statement

Users currently have no way to selectively enable or disable individual notification types. The only option is a global unsubscribe, which causes users to miss important transactional emails alongside unwanted marketing ones. Customer support receives roughly 200 monthly tickets related to unwanted notifications.

## Goals

- Allow users to enable or disable each notification category independently
- Persist notification preferences across sessions and devices
- Immediately reflect preference changes without requiring a page reload
- Give users visibility into all notification types the platform sends

## Non-Goals

- Push notifications (browser or mobile) are out of scope for this iteration
- Email template editing or custom notification content
- Notification scheduling or delivery-time preferences
- Per-notification-instance muting (e.g. muting a single thread)

## Requirements

### Functional Requirements

- **FR-01**: Users must be able to view all available notification categories and their current enabled/disabled state
- **FR-02**: Users must be able to toggle each notification category on or off independently
- **FR-03**: Preference changes must take effect for all future notifications without requiring re-login
- **FR-04**: Transactional notifications (password reset, billing receipts) must remain enabled and non-configurable
- **FR-05**: Users must receive a confirmation that their preferences have been saved

### Non-Functional Requirements

- **NFR-01**: Performance — preference changes must be reflected in subsequent notifications within 60 seconds
- **NFR-02**: Security — users may only view and modify their own notification preferences
- **NFR-03**: Reliability — preference data must not be lost during system updates or migrations
- **NFR-04**: Accessibility — the preferences interface must be keyboard-navigable and screen-reader compatible

## User Stories

- **US-01**: As a registered user, I want to disable marketing emails, so that I only receive notifications relevant to my account activity.
- **US-02**: As a registered user, I want to see all the types of emails the platform sends, so that I can make an informed decision about what to receive.
- **US-03**: As a user who previously unsubscribed from all emails, I want to re-enable individual categories, so that I can receive transactional emails without marketing ones.

## Acceptance Criteria

- [ ] **AC-01**: Given a logged-in user on the notification preferences page, When they toggle a notification category off and save, Then they no longer receive emails of that category
- [ ] **AC-02**: Given a logged-in user, When they view the preferences page, Then all notification categories are listed with their current enabled/disabled state accurately reflected
- [ ] **AC-03**: Given a user who disables a non-transactional notification category, When a system event of that type occurs, Then no email is sent for that event
- [ ] **AC-04**: Given a user who attempts to disable a transactional notification (e.g. password reset), Then the toggle is visually disabled and the user sees an explanation that it cannot be turned off
- [ ] **AC-05**: Given a logged-in user, When they save their preferences, Then a success confirmation is displayed

## Open Questions

1. Should notification preferences be exportable or visible to admins for compliance reasons?
2. What is the behaviour when a new notification category is introduced — should existing users default to enabled or disabled?
