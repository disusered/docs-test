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


def render_diagram(mmd_path: Path, output_dir: Path, init_block: str, formats: list[str] = None) -> bool:
    """Render a single .mmd file to SVG and/or PNG with theme prepended"""
    import subprocess

    if formats is None:
        formats = ["svg", "png"]

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
        outputs = []
        for fmt in formats:
            output_path = output_dir / f"{mmd_path.stem}.{fmt}"
            # Use scale=2 for crisp print output (PNG only)
            cmd = [
                "uv", "run", "mmdc",
                "-i", str(tmp_path),
                "-o", str(output_path),
                "-e", fmt,
                "-q",  # quiet
            ]
            if fmt == "png":
                cmd.extend(["-s", "2"])  # 2x scale for print

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  Error rendering {mmd_path.name} to {fmt}: {result.stderr}")
                return False
            outputs.append(output_path.name)
        print(f"  {mmd_path.name} -> {', '.join(outputs)}")
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

    print(f"Rendering {len(mmd_files)} diagram(s) to SVG + PNG...")
    success_count = 0
    for mmd_path in sorted(mmd_files):
        if render_diagram(mmd_path, DIAGRAMS_DIR, init_block):
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

            print(f"\nChange detected: {path.name}")
            render_diagram(path, DIAGRAMS_DIR, init_block)

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
