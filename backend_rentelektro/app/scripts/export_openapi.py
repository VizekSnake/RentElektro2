from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_project_root_on_path() -> None:
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)


def export_openapi(output_path: Path) -> None:
    _ensure_project_root_on_path()

    from app.core.config import get_settings
    from app.main import create_app

    app = create_app()
    schema = app.openapi()
    api_prefix = get_settings().API_V1_STR.rstrip("/")

    normalized_paths: dict[str, object] = {}
    for path, definition in schema.get("paths", {}).items():
        if api_prefix and path.startswith(f"{api_prefix}/"):
            normalized_path = path[len(api_prefix) :]
        elif api_prefix and path == api_prefix:
            normalized_path = "/"
        else:
            normalized_path = path
        normalized_paths[normalized_path] = definition
    schema["paths"] = normalized_paths

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export FastAPI OpenAPI schema to JSON.")
    parser.add_argument("--output", required=True, help="Path to output openapi.json.")
    args = parser.parse_args()

    export_openapi(Path(args.output).resolve())


if __name__ == "__main__":
    main()
