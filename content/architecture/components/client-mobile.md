---
title: Client Mobile
---

The Client Mobile application is the customer-facing mobile app for ticket purchasing.

## Overview

- **Type**: Client (Mobile Application)
- **Repository**: `xbol-app-client`
- **Platform**: React Native (iOS and Android)
- **Distribution**: App Store (iOS), Google Play (Android)

## Architecture

Architecture diagrams for mobile applications are planned for future documentation.

## Role

Provides customers with:

- Event browsing and search
- Interactive seat selection
- Ticket purchasing and checkout
- Mobile tickets with QR codes
- Push notification support

## API Integration

Communicates exclusively with [](./client-api) for all backend operations.

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Crash Reporting | Mobile app error monitoring and alerting |

See [](../index) for service inventory.
