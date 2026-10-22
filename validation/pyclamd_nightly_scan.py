# Python.ClamAV.json -> "ClamAV Python" [SecurityTools]
# Expected: import pyclamd
import sys
from pathlib import Path

import pyclamd


def scan_directory(root: Path) -> dict:
    daemon = pyclamd.ClamdAgnostic()
    if not daemon.ping():
        raise RuntimeError("clamd is not reachable")
    return daemon.multiscan_file(str(root)) or {}


if __name__ == "__main__":
    infected = scan_directory(Path(sys.argv[1]))
    for path, (status, signature) in infected.items():
        print(f"{status}\t{signature}\t{path}")
    sys.exit(1 if infected else 0)
