---
title: Handheld
---

The Handheld application is the staff-facing mobile app for ticket validation at venue gates.

## Overview

- **Type**: {term}`Client` (Mobile Application)
- **Repository**: `xbol-app-handheld`
- **{term}`Platform`**: React Native (Android only)
- **Distribution**: Side-loaded APK (not on app stores)

## Role

Provides gate staff with:

- QR code scanning for ticket validation
- Offline validation via {doc}`./bastion` connection
- Entry logging and statistics

## Network Mode

### Online Mode

Connects to {doc}`./client-api` through the internet for real-time validation.

### Offline Mode

Connects to local {doc}`./bastion` over LAN when internet is unavailable. Validation data syncs to cloud when connectivity resumes.

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
