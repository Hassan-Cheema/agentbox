"""Minimal example: run a snippet of Python in a sandboxed container.

Install first:  pip install -e .
Then run:       python examples/hello.py
"""

from agentbox import run_code

result = run_code(
    """
import sys
print("hello from inside the sandbox")
print("python:", sys.version.split()[0])
"""
)

print("stdout:   ", result["stdout"].rstrip())
print("stderr:   ", result["stderr"].rstrip())
print("exit_code:", result["exit_code"])
print("duration: ", result["duration_ms"], "ms")
