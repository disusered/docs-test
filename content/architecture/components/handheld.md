---
title: Handheld
---

The Handheld application is the staff-facing mobile app for ticket validation at venue gates.

## Overview

- **Type**: Client (Mobile Application)
- **Repository**: `xbol-app-handheld`
- **Platform**: React Native (Android only)
- **Distribution**: Side-loaded APK (not on app stores)

## Architecture

Architecture diagrams for mobile applications are planned for future documentation.

## Role

Provides gate staff with:

- QR code scanning for ticket validation
- Offline validation via [](./bastion) connection
- Entry logging and statistics

## Network Mode

### Online Mode

Connects to [](./client-api) through the internet for real-time validation.

### Offline Mode

Connects to local [](./bastion) over LAN when internet is unavailable. Validation data syncs to cloud when connectivity resumes.

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Crash Reporting | Mobile app error monitoring and alerting |

See [](../index) for service inventory.
