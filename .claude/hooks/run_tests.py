"""Stop hook: run the test suite before Claude is allowed to finish a turn.

Exit code 2 blocks the stop and feeds stderr back to Claude as its next instruction.
`stop_hook_active` is true when this hook already forced a continuation, so we
let that turn end to avoid an infinite loop.
"""

import json
import os
import subprocess
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    if payload.get("stop_hook_active"):
        return 0
    cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if not os.path.exists(os.path.join(cwd, "tests")):
        return 0
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return 0
    if result.returncode == 5:  # no tests collected
        return 0
    summary = "\n".join(result.stdout.strip().splitlines()[-15:])
    print(
        "Tests are failing. Fix them before finishing, and show the passing run.\n"
        + summary,
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
