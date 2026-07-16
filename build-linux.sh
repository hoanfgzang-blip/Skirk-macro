#!/usr/bin/env bash
set -euo pipefail

echo "==================================="
echo "  Building Cryss for Linux"
echo "==================================="

mkdir -p build

echo
echo "[1/2] Building Python backend (Cryss)..."
(
  cd build
  pyinstaller --onefile --name Cryss --workpath temp --distpath dist ../src/macro/main.py
)

echo
echo "[2/2] Building Electron UI..."
rm -rf build/app-linux
(
  cd src/UI
  pnpm package:linux
)

echo
echo "==================================="
echo "  BUILD SUCCESSFUL!"
echo "  App is located in: build/app-linux/linux-unpacked/Cryss"
echo "==================================="
