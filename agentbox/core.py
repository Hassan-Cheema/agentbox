"""Run untrusted Python code in a one-shot Docker container."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

import docker
from docker.errors import APIError, DockerException, ImageNotFound
from requests.exceptions import ReadTimeout

IMAGE = "python:3.11-slim"


class DockerUnavailableError(RuntimeError):
    """Raised when the Docker daemon cannot be reached."""


def _connect() -> docker.DockerClient:
    try:
        return docker.from_env()
    except DockerException as e:
        raise DockerUnavailableError(
            "Cannot reach the Docker daemon. Is Docker Desktop running? "
            "Verify with `docker version`."
        ) from e


def run_code(code: str, timeout: int = 30) -> dict:
    """
    Execute Python code in an isolated Docker container.
    Returns: {"stdout": str, "stderr": str, "exit_code": int, "duration_ms": int}
    """
    client = _connect()

    # Make sure the image is present so the first call has a predictable error
    # rather than a confusing 404 from the daemon.
    try:
        client.images.get(IMAGE)
    except ImageNotFound:
        client.images.pull(IMAGE)

    start = time.monotonic()

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "script.py"
        script_path.write_text(code, encoding="utf-8")

        container = client.containers.run(
            image=IMAGE,
            command=["python", "/sandbox/script.py"],
            volumes={tmpdir: {"bind": "/sandbox", "mode": "ro"}},
            working_dir="/sandbox",
            detach=True,
            network_disabled=True,
            mem_limit="256m",
            pids_limit=128,
            stdout=True,
            stderr=True,
        )

        timed_out = False
        exit_code = -1
        try:
            try:
                result = container.wait(timeout=timeout)
                exit_code = int(result.get("StatusCode", -1))
            except ReadTimeout:
                # docker-py raises requests.exceptions.ReadTimeout when wait()
                # exceeds the client-side timeout. Kill the container so it
                # doesn't keep burning resources.
                timed_out = True
                try:
                    container.kill()
                except APIError:
                    # Container may have exited between wait() and kill().
                    pass

            stdout = container.logs(stdout=True, stderr=False).decode(
                "utf-8", errors="replace"
            )
            stderr = container.logs(stdout=False, stderr=True).decode(
                "utf-8", errors="replace"
            )
        finally:
            try:
                container.remove(force=True)
            except APIError:
                pass

    if timed_out:
        stderr = (stderr + f"\n[agentbox] execution timed out after {timeout}s").lstrip("\n")
        exit_code = -1

    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "duration_ms": int((time.monotonic() - start) * 1000),
    }
