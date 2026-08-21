from __future__ import annotations
import base64
from dataclasses import asdict
from pathlib import Path
from grok_cua.core.models import Expectation
from grok_cua.core.verifier import verify

_adapter = None
_last_obs = None

def get_adapter():
    global _adapter
    if _adapter is None:
        from grok_cua.adapters.windows import WindowsAdapter
        _adapter = WindowsAdapter()
    return _adapter

def main():
    try:
        from mcp.server import MCPServer
        from mcp.types import ImageContent, TextContent
        Server = MCPServer
    except ImportError:
        # Compatibility with MCP Python SDK v1 if a user pins it.
        try:
            from mcp.server.fastmcp import FastMCP
            from mcp.types import ImageContent, TextContent
            Server = FastMCP
        except ImportError as e:
            raise SystemExit("Install dependencies first: pip install -e '.[windows]'") from e

    mcp = Server("grok-computer-use")

    @mcp.tool()
    def observe(include_screenshot: bool = False, max_controls: int = 220) -> dict:
        """Observe foreground window and semantic Windows UIA controls."""
        global _last_obs
        obs = get_adapter().observe(max_controls=max_controls, screenshot=include_screenshot)
        _last_obs = obs
        return asdict(obs)

    @mcp.tool()
    def list_windows() -> list[dict]:
        """List top-level windows with process names."""
        return get_adapter().list_windows()

    @mcp.tool()
    def activate_window(query: str) -> dict:
        """Activate a window by partial title or process name."""
        return {"ok": get_adapter().activate_window(query)}

    @mcp.tool()
    def open_app(executable: str, args: list[str] | None = None) -> dict:
        """Launch an executable directly without invoking a command shell."""
        return {"ok": True, "pid": get_adapter().open_app(executable, args or [])}

    @mcp.tool()
    def find_controls(query: str, role: str | None = None) -> list[dict]:
        """Find controls by visible label/automation id and optional role."""
        return [asdict(c) for c in get_adapter().find(query, role)]

    @mcp.tool()
    def click_control(name: str, role: str | None = None, exact: bool = False) -> dict:
        """Semantically re-resolve and click a unique UIA control. Prefer this over coordinates."""
        return get_adapter().click_control(name, role, exact)

    @mcp.tool()
    def click_xy(x: int, y: int) -> dict:
        """Fallback coordinate click. Use only when semantic control targeting fails."""
        get_adapter().click_xy(x, y)
        return {"ok": True}

    @mcp.tool()
    def type_text(text: str) -> dict:
        """Paste text into the focused control; supports Unicode."""
        get_adapter().type_text(text)
        return {"ok": True, "chars": len(text)}

    @mcp.tool()
    def hotkey(keys: list[str]) -> dict:
        """Press a chord such as ['ctrl','l'] or ['alt','tab']."""
        get_adapter().hotkey(keys)
        return {"ok": True}

    @mcp.tool()
    def scroll(amount: int) -> dict:
        """Scroll foreground UI; positive is up, negative is down."""
        get_adapter().scroll(amount)
        return {"ok": True}

    @mcp.tool()
    def screenshot():
        """Capture desktop and return the actual image to the model, plus local path."""
        path = Path(get_adapter().screenshot())
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return [
            TextContent(type="text", text=f"Screenshot captured: {path}"),
            ImageContent(type="image", data=data, mime_type="image/png"),
        ]

    @mcp.tool()
    def verify_state(active_window_contains: str | None = None,
                     ui_text_contains: str | None = None,
                     control_role: str | None = None,
                     process_running: str | None = None,
                     state_changed: bool = False) -> dict:
        """Re-observe and deterministically verify expected postconditions after a state change."""
        global _last_obs
        before = _last_obs
        after = get_adapter().observe(max_controls=260, screenshot=False)
        exp = Expectation(active_window_contains=active_window_contains,
                          ui_text_contains=ui_text_contains,
                          control_role=control_role,
                          process_running=process_running,
                          state_changed=state_changed)
        result = verify(before, after, exp)
        _last_obs = after
        return asdict(result)

    mcp.run()

if __name__ == "__main__":
    main()
