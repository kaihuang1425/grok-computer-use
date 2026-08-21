# Competitive thesis

The goal is not to claim universal SOTA immediately. The first measurable wedge is Windows cross-application reliability.

## Baselines

- Claude Computer Use: strong vision/action loop; proprietary model-grounding advantage.
- Codex Computer Use: strong product integration, browser/tool routing and permissions.
- Microsoft UFO²: strongest directly comparable Windows-native architecture: UIA + native APIs + visual fallback + MCP + app agents.
- Agent S3: very strong OSWorld performance through agent architecture and Best-of-N scaling.
- UI-TARS: strong native GUI grounding.
- Fara 1.5: strong browser agent plus serious verifier/evaluation stack.

## Where to win

1. Verification-first execution: every consequential state transition carries an explicit postcondition and deterministic evidence when available.
2. Cross-app checkpoint evidence: persist artifacts and evidence between applications, not just screenshots/conversation memory.
3. Hybrid routing with failure-aware escalation: API/shell/browser/UIA/vision/coordinates chosen by reliability and disruption, and switched after classified failure.
4. Grok-native distribution: `.grok` skill + local stdio MCP + Grok permissions, without needing a separate agent UI.
5. Non-disruptive execution (next): isolated Windows worker desktop/VM and live intervention rather than taking over the user's active pointer.
6. Learned capability registry (next): per-app successful routes and verifier recipes, with confidence decay when app versions change.

## Do not compete on

- Raw ScreenSpot grounding alone: specialist grounding models will usually win.
- Browser-only automation: crowded and mature.
- A huge monolithic multi-agent graph before the verifier and recovery loop are proven.
