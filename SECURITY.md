# Security

Grok CUA Lab can control a Windows desktop. Treat it as privileged local automation software.

## Trust boundary

- Run the MCP server locally over stdio. Do not expose it directly to the public internet.
- Use a dedicated Windows account, VM, or isolated desktop for untrusted tasks.
- Keep Grok/tool permissions at the narrowest practical scope.
- Do not grant administrator privileges unless a specific task requires them.
- Stop on unexpected authentication, UAC, payment, credential, or privacy-sensitive dialogs.

## Tool design

`open_app` launches an executable directly with `shell=False`; it does not accept a shell command string. This reduces accidental command-shell injection, but any executable granted to an agent can still have powerful effects.

Coordinate input and clipboard-based typing are fallbacks. Semantic UI Automation and deterministic APIs should be preferred because they are easier to constrain and verify.

## Reporting

Do not open a public issue containing tokens, credentials, screenshots with private data, or sensitive traces. Report security concerns privately to the repository owner through GitHub's private vulnerability reporting if enabled.
