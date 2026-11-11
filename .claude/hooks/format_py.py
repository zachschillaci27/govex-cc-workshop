"""PostToolUse hook: run `ruff format` on any .py file Claude just edited or wrote.

Skips silently when ruff is not installed, so the hook never blocks work.
"""

import json
import shutil
import subprocess
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = payload.get("tool_input", {}).get("file_path", "")
    if not path.endswith(".py") or shutil.which("ruff") is None:
        return 0
    subprocess.run(["ruff", "format", "--quiet", path], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
