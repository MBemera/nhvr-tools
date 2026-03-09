#!/usr/bin/env python3
"""
NHVR Tools — Setup Wizard
==========================
One-command setup for non-technical users.
Run: python setup.py
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import time

# ── Colours (disabled on Windows unless WT is present) ────────────────────────
USE_COLOR = sys.stdout.isatty() and (
    os.name != "nt" or os.environ.get("WT_SESSION")
)

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def green(t: str) -> str:  return _c("32", t)
def yellow(t: str) -> str: return _c("33", t)
def red(t: str) -> str:    return _c("31", t)
def bold(t: str) -> str:   return _c("1", t)
def cyan(t: str) -> str:   return _c("36", t)
def dim(t: str) -> str:    return _c("2", t)


# ── Helpers ───────────────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def banner() -> None:
    print()
    print(bold("=" * 56))
    print(bold("   NHVR Tools — Setup Wizard"))
    print(bold("   Heavy Vehicle Compliance MCP Server"))
    print(bold("=" * 56))
    print()
    print("  This wizard will get everything set up for you.")
    print("  Just answer a few simple questions — press Enter")
    print("  to accept the default shown in [brackets].")
    print()


def ask_yes_no(question: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"  {question} {hint} ").strip().lower()
        if answer == "":
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(f"  {yellow('Please type y or n.')}")


def ask_text(question: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    answer = input(f"  {question}{hint} ").strip()
    return answer if answer else default


def step(number: int, title: str) -> None:
    print()
    print(f"  {bold(cyan(f'Step {number}'))}  {bold(title)}")
    print(f"  {'─' * 48}")


def ok(msg: str) -> None:
    print(f"  {green('✓')} {msg}")


def warn(msg: str) -> None:
    print(f"  {yellow('!')} {msg}")


def fail(msg: str) -> None:
    print(f"  {red('✗')} {msg}")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


# ── Step 1: Python version check ─────────────────────────────────────────────
def check_python() -> bool:
    step(1, "Checking Python version")
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v >= (3, 10):
        ok(f"Python {version_str} — looks good!")
        return True
    else:
        fail(f"Python {version_str} found, but 3.10+ is required.")
        print()
        print("  Please install Python 3.10 or newer:")
        print(f"  {cyan('https://www.python.org/downloads/')}")
        return False


# ── Step 2: Install dependencies ─────────────────────────────────────────────
def install_dependencies() -> bool:
    step(2, "Installing dependencies")
    print("  This may take a minute or two...")
    print()

    result = run(
        [sys.executable, "-m", "pip", "install", "-e", PROJECT_DIR],
        cwd=PROJECT_DIR,
    )
    if result.returncode == 0:
        ok("All Python packages installed.")
        return True
    else:
        fail("pip install failed. Details:")
        for line in result.stderr.strip().splitlines()[-5:]:
            print(f"    {line}")
        print()
        print(f"  Try running manually: {cyan('pip install -e .')}")
        return False


# ── Step 3: Playwright browser (optional) ────────────────────────────────────
def install_playwright() -> None:
    step(3, "Playwright browser (optional)")
    print(textwrap.indent(textwrap.dedent("""\
        Some advanced features can scrape JavaScript-heavy
        pages using a real browser. This downloads Chromium
        (~150 MB). Most users don't need this right away —
        you can always install it later.
    """), "  "))

    if not ask_yes_no("Install Playwright browser now?", default=False):
        warn("Skipped — you can run this later:")
        print(f"    {cyan('playwright install chromium')}")
        return

    print("  Downloading Chromium (this may take a moment)...")
    result = run([sys.executable, "-m", "playwright", "install", "chromium"])
    if result.returncode == 0:
        ok("Chromium installed.")
    else:
        warn("Could not install Chromium automatically.")
        print(f"  Run later: {cyan('playwright install chromium')}")


# ── Step 4: API key (optional) ───────────────────────────────────────────────
def configure_api_key() -> str | None:
    step(4, "NHVR API key (optional)")
    print(textwrap.indent(textwrap.dedent("""\
        If you have an NHVR API key, you can enter it now
        to enable vehicle registration lookups. If you
        don't have one, just press Enter to skip — all
        other features will work without it.
    """), "  "))

    key = ask_text("NHVR API key (or Enter to skip):")
    if key:
        ok("API key saved — it will be included in your config.")
        return key
    else:
        warn("Skipped — registration lookups won't be available.")
        return None


# ── Step 5: Claude Desktop config ────────────────────────────────────────────
def get_claude_config_path() -> str:
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser(
            "~/Library/Application Support/Claude/claude_desktop_config.json"
        )
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        return os.path.join(appdata, "Claude", "claude_desktop_config.json")
    else:  # Linux
        return os.path.expanduser(
            "~/.config/Claude/claude_desktop_config.json"
        )


def configure_claude_desktop(api_key: str | None) -> None:
    step(5, "Connect to Claude Desktop")

    config_path = get_claude_config_path()
    python_path = shutil.which("python3") or shutil.which("python") or sys.executable
    server_module = os.path.join(PROJECT_DIR, "nhvr_mcp", "server.py")

    # Build the server entry
    server_entry: dict = {
        "command": python_path,
        "args": [server_module],
    }
    if api_key:
        server_entry["env"] = {"NHVR_API_KEY": api_key}

    print(textwrap.indent(textwrap.dedent("""\
        To use NHVR Tools in Claude Desktop, we need to add
        it to Claude's configuration file.
    """), "  "))

    print(f"  Config file: {cyan(config_path)}")
    print()

    if ask_yes_no("Automatically add NHVR Tools to Claude Desktop?"):
        # Read existing config or start fresh
        config: dict = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                ok("Found existing Claude config.")
            except (json.JSONDecodeError, OSError):
                warn("Existing config was unreadable — creating a new one.")
                # Back up the broken file
                backup = config_path + ".backup"
                try:
                    shutil.copy2(config_path, backup)
                    ok(f"Old config backed up to {backup}")
                except OSError:
                    pass

        # Ensure mcpServers key exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Check if already configured
        if "nhvr-tools" in config["mcpServers"]:
            if not ask_yes_no("NHVR Tools is already configured. Overwrite?", default=False):
                ok("Kept existing configuration.")
                return

        config["mcpServers"]["nhvr-tools"] = server_entry

        # Write config
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            ok("Claude Desktop configured!")
            print()
            print(f"  {yellow('Restart Claude Desktop to activate NHVR Tools.')}")
        except OSError as e:
            fail(f"Could not write config: {e}")
            print()
            _print_manual_config(server_entry)
    else:
        _print_manual_config(server_entry)


def _print_manual_config(server_entry: dict) -> None:
    print()
    print("  Add the following to your Claude Desktop config")
    print(f"  inside the {cyan('\"mcpServers\"')} section:")
    print()
    snippet = json.dumps({"nhvr-tools": server_entry}, indent=2)
    for line in snippet.splitlines():
        print(f"    {line}")
    print()
    print(f"  Config location: {cyan(get_claude_config_path())}")


# ── Step 6: Quick test ───────────────────────────────────────────────────────
def test_server() -> bool:
    step(6, "Quick test")
    print("  Checking the server can start...")

    # Import check — can we load the module?
    result = run(
        [sys.executable, "-c", "from nhvr_mcp.server import mcp; print('ok')"],
        cwd=PROJECT_DIR,
    )
    if result.returncode == 0 and "ok" in result.stdout:
        ok("Server module loads correctly.")
    else:
        fail("Server module failed to load.")
        if result.stderr:
            for line in result.stderr.strip().splitlines()[-5:]:
                print(f"    {line}")
        return False

    # CLI check
    result = run(
        [sys.executable, "-m", "nhvr_mcp.cli", "--help"],
        cwd=PROJECT_DIR,
    )
    if result.returncode == 0:
        ok("CLI is working.")
    else:
        warn("CLI check had issues (non-critical).")

    return True


# ── Done! ─────────────────────────────────────────────────────────────────────
def finish() -> None:
    print()
    print(bold("=" * 56))
    print(bold(green("   Setup complete!")))
    print(bold("=" * 56))
    print()
    print("  What to do next:")
    print()
    print(f"  1. {bold('Restart Claude Desktop')} to load NHVR Tools")
    print(f"  2. Ask Claude about heavy vehicle regulations, e.g.:")
    print(f'     {cyan("What are the fatigue rules for standard hours?")}')
    print(f'     {cyan("What are the mass limits for a semi-trailer?")}')
    print(f'     {cyan("Explain chain of responsibility duties")}')
    print()
    print("  You can also use the CLI directly:")
    print(f"    {cyan('nhvr fatigue rules')}")
    print(f"    {cyan('nhvr mass limits')}")
    print(f"    {cyan('nhvr --help')}")
    print()
    print(f"  Need help? See the README: {cyan('README.md')}")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    banner()

    # Step 1: Python check
    if not check_python():
        sys.exit(1)

    # Step 2: Install dependencies
    if not install_dependencies():
        print()
        if not ask_yes_no("Continue anyway?", default=False):
            sys.exit(1)

    # Step 3: Playwright (optional)
    install_playwright()

    # Step 4: API key (optional)
    api_key = configure_api_key()

    # Step 5: Claude Desktop config
    configure_claude_desktop(api_key)

    # Step 6: Test
    test_server()

    # Done!
    finish()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"\n  {yellow('Setup cancelled. You can run it again anytime:')}")
        print(f"  {cyan('python setup.py')}")
        print()
        sys.exit(130)
