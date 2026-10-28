#!/usr/bin/env python3
"""Entry point do CLI Didatik."""

import os
import sys

_py_v = f"{sys.version_info.major}.{sys.version_info.minor}"
if sys.version_info < (3, 13):
    print(f"\n[ERRO CRÍTICO] Didatik exige Python 3.13+.")
    print(f"Versão detectada: Python {_py_v}")
    print("Para corrigir, reinstale forçando a versão:")
    print("  uv tool install --force --python 3.13 <fonte-do-didatik>")
    sys.exit(1)

for _v in ("VIRTUAL_ENV", "PYTHONHOME", "PYTHONPATH"):
    _ = os.environ.pop(_v, None)

for _p in ("", "."):
    while _p in sys.path:
        sys.path.remove(_p)

from didatik.cli import app


def main() -> None:
    app()


if __name__ == "__main__":
    main()
