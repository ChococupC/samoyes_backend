import importlib
from pathlib import Path
from fastapi import APIRouter


def auto_load_routers(app_router: APIRouter, base_path: Path):
    for app_folder in base_path.iterdir():
        if not app_folder.is_dir():
            continue

        api_file = app_folder / "api.py"
        if api_file.exists():
            module_path = ".".join(api_file.with_suffix("").parts[-3:])
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "router"):
                    app_router.include_router(module.router)
                    print(f"Loaded router from {module_path}")
            except Exception as e:
                print(f"Failed to load {module_path}: {e}")