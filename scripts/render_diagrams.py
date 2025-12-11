#!/usr/bin/env python3
"""
Render Mermaid diagrams with theme from _terms.yml

Usage:
    uv run render-diagrams              # One-shot render all diagrams
    uv run render-diagrams --watch      # Watch mode with live reload
    uv run render-diagrams context      # Render specific diagram(s)
"""

import argparse
import sys
import tempfile
import time
from pathlib import Path

import yaml

# Project root (where _terms.yml lives)
PROJECT_ROOT = Path(__file__).parent.parent
DIAGRAMS_DIR = PROJECT_ROOT / "diagrams"
TERMS_FILE = PROJECT_ROOT / "_terms.yml"


def load_mermaid_init() -> str:
    """Load the mermaid init block from _terms.yml"""
    if not TERMS_FILE.exists():
        print(f"Warning: {TERMS_FILE} not found, using default theme")
        return ""

    with open(TERMS_FILE) as f:
        terms = yaml.safe_load(f)

    init_block = terms.get("mermaid_init", "")
    if not init_block:
        print("Warning: mermaid_init not found in _terms.yml, using default theme")
        return ""

    return init_block.strip() + "\n"


def render_diagram(mmd_path: Path, svg_path: Path, init_block: str) -> bool:
    """Render a single .mmd file to .svg with theme prepended"""
    try:
        from mermaid_cli import render_mermaid_file_sync
    except ImportError:
        print("Error: mermaid-cli not installed. Run: uv sync --extra diagrams")
        print("Then run: uv run playwright install chromium")
        return False

    # Read original content
    content = mmd_path.read_text()

    # Prepend init block if not already present
    if not content.strip().startswith("%%{init"):
        content = init_block + content

    # Write to temp file and render
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False
    ) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        render_mermaid_file_sync(
            input_file=str(tmp_path),
            output_file=str(svg_path),
            output_format="svg",
        )
        print(f"  {mmd_path.name} -> {svg_path.name}")
        return True
    except Exception as e:
        print(f"  Error rendering {mmd_path.name}: {e}")
        return False
    finally:
        tmp_path.unlink(missing_ok=True)


def render_all(patterns: list[str] | None = None) -> int:
    """Render all diagrams (or specific ones if patterns provided)"""
    if not DIAGRAMS_DIR.exists():
        print(f"Error: {DIAGRAMS_DIR} directory not found")
        return 1

    init_block = load_mermaid_init()

    # Find .mmd files
    if patterns:
        mmd_files = []
        for pattern in patterns:
            # Allow specifying with or without .mmd extension
            if not pattern.endswith(".mmd"):
                pattern = f"{pattern}.mmd"
            matches = list(DIAGRAMS_DIR.glob(pattern))
            mmd_files.extend(matches)
    else:
        mmd_files = list(DIAGRAMS_DIR.glob("*.mmd"))

    if not mmd_files:
        print("No .mmd files found to render")
        return 0

    print(f"Rendering {len(mmd_files)} diagram(s)...")
    success_count = 0
    for mmd_path in sorted(mmd_files):
        svg_path = mmd_path.with_suffix(".svg")
        if render_diagram(mmd_path, svg_path, init_block):
            success_count += 1

    print(f"Done: {success_count}/{len(mmd_files)} diagrams rendered")
    return 0 if success_count == len(mmd_files) else 1


def watch_diagrams() -> None:
    """Watch for changes and re-render automatically"""
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        print("Error: watchdog not installed. Run: uv sync --extra diagrams")
        sys.exit(1)

    init_block = load_mermaid_init()

    class MermaidHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_render = {}

        def on_modified(self, event):
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix != ".mmd":
                return

            # Debounce: skip if rendered within last second
            now = time.time()
            if path in self.last_render and now - self.last_render[path] < 1:
                return
            self.last_render[path] = now

            svg_path = path.with_suffix(".svg")
            print(f"\nChange detected: {path.name}")
            render_diagram(path, svg_path, init_block)

    if not DIAGRAMS_DIR.exists():
        print(f"Error: {DIAGRAMS_DIR} directory not found")
        sys.exit(1)

    # Initial render
    print("Initial render...")
    render_all()

    # Start watching
    print(f"\nWatching {DIAGRAMS_DIR} for changes... (Ctrl+C to stop)")
    observer = Observer()
    observer.schedule(MermaidHandler(), str(DIAGRAMS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching")
    observer.join()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Mermaid diagrams with consistent theming"
    )
    parser.add_argument(
        "diagrams",
        nargs="*",
        help="Specific diagrams to render (default: all)",
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch for changes and re-render automatically",
    )
    args = parser.parse_args()

    if args.watch:
        watch_diagrams()
        return 0
    else:
        return render_all(args.diagrams if args.diagrams else None)


if __name__ == "__main__":
    sys.exit(main())
