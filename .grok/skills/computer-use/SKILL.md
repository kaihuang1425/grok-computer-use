---
name: computer-use
description: Verification-first Windows desktop control through the grok-computer-use MCP. Use for native desktop tasks, especially cross-application workflows.
when-to-use: computer use, desktop automation, Windows app interaction, click/type in an application, cross-app workflow
user-invocable: true
metadata:
  author: grok-cua-lab
  short-description: Verified hybrid Windows computer use
---

# Computer Use

Use the least fragile execution surface available.

Priority: native API/MCP > shell/filesystem > browser DOM/CDP > Windows UIA > screenshot vision > raw coordinates.

## Mandatory execution loop

For every meaningful state transition:

1. Observe the target application.
2. State the immediate subgoal and an observable postcondition.
3. Prefer semantic UIA controls; do not use coordinates if a stable UIA control exists.
4. Execute one meaningful state transition.
5. Call `grok-computer-use__verify_state` with a concrete postcondition.
6. If verification fails, classify the failure before retrying:
   - stale element / state changed unexpectedly -> re-observe and re-resolve
   - target absent from UIA -> use screenshot/vision fallback
   - wrong app/window -> recover focus
   - repeated no-op -> choose a different execution route, not the same click
7. Do not declare success until final postconditions are verified.

## Cross-application tasks

Break the request into checkpoints. Before leaving an app, verify the artifact/state that the next app depends on. Carry forward exact evidence (file path, selected value, copied text, window title) rather than relying on memory of the visual state.

## Safety

Do not perform destructive, irreversible, financial, credential, privacy-sensitive, or externally consequential actions without the user's explicit approval at the point of action. Stop on unexpected authentication/UAC dialogs.

## Efficiency

Avoid repeated screenshots when UIA already exposes the needed state. Batch only actions whose intermediate state cannot change the next action. If an action can be executed deterministically through an API/shell command, do not simulate human input merely for appearance.
