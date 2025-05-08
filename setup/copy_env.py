#!/usr/bin/env python3
# copy_env.py

import os
import shutil
from settings import settings

def find_project_root(marker='requirements.txt'):
    root = os.path.abspath(os.path.dirname(__file__))
    while not os.path.isfile(os.path.join(root, marker)):
        parent = os.path.dirname(root)
        if parent == root:
            raise FileNotFoundError(f"Could not find {marker} in any parent directory.")
        root = parent
    return root

def copy_env():
    if not getattr(settings, 'COPY_ENV_TO_PROJECT_ROOT', False):
        print("COPY_ENV_TO_PROJECT_ROOT is False; skipping copy.")
        return
    src = settings.OUTPUT_ENV_FILE_NAME
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Source env file not found: {src}")
    project_root = find_project_root()
    dest = os.path.join(project_root, '.env')
    shutil.copy(src, dest)
    print(f"✔ {src} copied to project root as .env")

if __name__ == '__main__':
    copy_env()
