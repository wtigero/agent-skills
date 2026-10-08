---
name: verify-project
description: Verify the local invoice API and its export contract using the existing Python wire harness.
---

# Verify invoice project

Status: validated for the original fixture; rerun after relevant changes.

## Launch

The harness starts an owned local server on an ephemeral port.

## Doctor

Run `python --version`; this fixture requires Python 3.9+ and no extra packages.

## Drive

Read [the invoice route](references/invoice.md) and run its command from repo root.

## Evidence

The harness saves the actual response and consumer assertion at the requested path.

## Cleanup

The harness stops its owned server. Check `server_stopped` in the saved receipt.
