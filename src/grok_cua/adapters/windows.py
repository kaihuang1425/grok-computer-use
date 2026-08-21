from __future__ import annotations
import platform, subprocess, time
from pathlib import Path
from typing import Iterable
from grok_cua.core.models import Control, Observation

class WindowsAdapter:
    """Windows UIA + input adapter. Windows-only libraries are imported lazily."""

    def __init__(self, artifact_dir: str = ".grok-cua-artifacts"):
        if platform.system() != "Windows":
            raise RuntimeError("WindowsAdapter requires Windows 10/11 or Windows Server")
        self.artifact_dir = Path(artifact_dir)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        import uiautomation as auto
        self.auto = auto

    def _process_name(self, pid: int | str | None) -> str:
        if not pid:
            return ""
        try:
            import psutil
            return psutil.Process(int(pid)).name()
        except Exception:
            return str(pid)

    def _control(self, c, idx: int) -> Control:
        rect = getattr(c, "BoundingRectangle", None)
        bounds = None
        try:
            bounds = (int(rect.left), int(rect.top), int(rect.right), int(rect.bottom))
        except Exception:
            pass
        return Control(
            id=f"uia:{idx}:{getattr(c, 'AutomationId', '')}:{getattr(c, 'ControlTypeName', '')}",
            name=getattr(c, "Name", "") or "",
            role=(getattr(c, "ControlTypeName", "") or "").replace("Control", "").lower(),
            automation_id=getattr(c, "AutomationId", "") or "",
            enabled=bool(getattr(c, "IsEnabled", True)),
            visible=not bool(getattr(c, "IsOffscreen", False)),
            bounds=bounds,
        )

    def observe(self, max_controls: int = 220, screenshot: bool = False) -> Observation:
        root = self.auto.GetForegroundControl()
        controls: list[Control] = []
        if root:
            try:
                queue = list(root.GetChildren())
                idx = 0
                while queue and len(controls) < max_controls:
                    c = queue.pop(0)
                    controls.append(self._control(c, idx)); idx += 1
                    try:
                        queue.extend(c.GetChildren())
                    except Exception:
                        pass
            except Exception:
                pass
        shot = self.screenshot() if screenshot else None
        pid = getattr(root, "ProcessId", None) if root else None
        return Observation(
            active_window=(getattr(root, "Name", "") or "") if root else "",
            process=self._process_name(pid),
            controls=controls,
            screenshot_path=shot,
        )

    def screenshot(self) -> str:
        import mss
        from PIL import Image
        ts = int(time.time() * 1000)
        path = self.artifact_dir / f"screen-{ts}.png"
        with mss.mss() as sct:
            mon = sct.monitors[0]
            raw = sct.grab(mon)
            Image.frombytes("RGB", raw.size, raw.rgb).save(path)
        return str(path.resolve())

    def list_windows(self) -> list[dict]:
        desktop = self.auto.GetRootControl()
        out=[]
        try:
            for c in desktop.GetChildren():
                name=getattr(c,"Name","") or ""
                if not name:
                    continue
                pid=getattr(c,"ProcessId",None)
                out.append({"name": name, "process": self._process_name(pid), "pid": pid})
        except Exception:
            pass
        return out[:100]

    def activate_window(self, query: str) -> bool:
        q=query.lower()
        desktop=self.auto.GetRootControl()
        try:
            for c in desktop.GetChildren():
                name=(getattr(c,"Name","") or "")
                proc=self._process_name(getattr(c,"ProcessId",None))
                if q in name.lower() or q in proc.lower():
                    try:
                        c.SetActive(); return True
                    except Exception:
                        try:
                            c.SetFocus(); return True
                        except Exception:
                            return False
        except Exception:
            pass
        return False

    def open_app(self, executable: str, args: list[str] | None = None) -> int:
        argv = [executable, *(args or [])]
        p = subprocess.Popen(argv, shell=False)
        return p.pid

    def click_xy(self, x: int, y: int) -> None:
        import pyautogui
        pyautogui.click(x=x, y=y)

    def type_text(self, text: str, interval: float = 0.0) -> None:
        import pyautogui, pyperclip
        # Clipboard paste handles Unicode reliably; restore previous clipboard when possible.
        previous = None
        try:
            previous = pyperclip.paste()
        except Exception:
            pass
        try:
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
        finally:
            if previous is not None:
                try: pyperclip.copy(previous)
                except Exception: pass

    def hotkey(self, keys: Iterable[str]) -> None:
        import pyautogui
        pyautogui.hotkey(*list(keys))

    def scroll(self, amount: int) -> None:
        import pyautogui
        pyautogui.scroll(amount)

    def find(self, query: str, role: str | None = None, max_controls: int = 300) -> list[Control]:
        obs = self.observe(max_controls=max_controls, screenshot=False)
        q = query.lower()
        out = [c for c in obs.controls if q in (c.name + " " + c.automation_id).lower()]
        if role:
            out = [c for c in out if role.lower() == c.role.lower()]
        return out[:30]

    def click_control(self, name: str, role: str | None = None, exact: bool = False) -> dict:
        """Re-resolve by semantic identity at execution time to avoid stale coordinates."""
        root = self.auto.GetForegroundControl()
        if not root:
            return {"ok": False, "reason": "no foreground control"}
        queue = list(root.GetChildren())
        q = name.lower()
        matches=[]
        while queue:
            c = queue.pop(0)
            cname = (getattr(c, "Name", "") or "")
            ctype = (getattr(c, "ControlTypeName", "") or "").replace("Control", "").lower()
            hit = cname.lower() == q if exact else q in cname.lower()
            if hit and (not role or role.lower() == ctype):
                matches.append(c)
            try:
                queue.extend(c.GetChildren())
            except Exception:
                pass
        if len(matches) != 1:
            return {"ok": False, "reason": f"expected one semantic match, found {len(matches)}"}
        c=matches[0]
        try:
            c.Click(simulateMove=False)
            return {"ok": True, "name": getattr(c,"Name","")}
        except Exception as e:
            return {"ok": False, "reason": f"UIA click failed: {e}"}
