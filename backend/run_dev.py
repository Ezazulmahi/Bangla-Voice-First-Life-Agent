"""Dev entrypoint that's safe to invoke from any working directory (used by
.claude/launch.json, which can't set a subprocess cwd)."""

import os
import sys

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[BACKEND_DIR])
