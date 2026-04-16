# Agentbox

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-v0%20wip-orange.svg)

Run untrusted Python in a one-shot Docker sandbox.

## Quickstart

```bash
pip install -e .                       # needs Docker running locally
python examples/hello.py
```

```python
from agentbox import run_code
print(run_code("print(1 + 1)"))
# {'stdout': '2\n', 'stderr': '', 'exit_code': 0, 'duration_ms': ...}
```

## Contributing

Contributions welcome. Open an issue before starting significant work.
