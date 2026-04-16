# agentbox

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-v0%20wip-orange.svg)

Open-source sandbox runtime for AI agents.

Run untrusted Python in a one-shot Docker sandbox. v0 is Docker-based. Next: Firecracker microVMs for sub-200ms cold starts, session forking, deterministic replay.

## Quickstart

```bash
pip install -e .
python examples/hello.py
```

```python
from agentbox import run_code

result = run_code("print(1 + 1)")
print(result)
# {'stdout': '2\n', 'stderr': '', 'exit_code': 0, 'duration_ms': ...}
```

## Status

v0 — Docker-based, single-shot execution. Work in progress. Building in public.

## License

MIT
