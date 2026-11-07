# Build RAVEN on Windows 11

## Prerequisites

- Visual Studio 2022 Build Tools with **Desktop development with C++**
- CMake 3.24+
- Python 3.11+
- Git

## Start the local workbench

From the repository root:

```powershell
cd raven
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8765
```

Open http://127.0.0.1:8765. The service binds to loopback only.

## Build the C++ core

```powershell
cmake -S core -B build\raven-core -A x64
cmake --build build\raven-core --config Release
ctest --test-dir build\raven-core -C Release --output-on-failure
```

The core currently provides deterministic, explainable evidence ranking. It does not require llama.cpp or a downloaded model.

## llama.cpp integration

The parent repository remains the local inference runtime. RAVEN's adapter will be optional and isolated. Do not assume a text model can perform visual geolocation; image feature extraction and geographic ranking are separate components.
