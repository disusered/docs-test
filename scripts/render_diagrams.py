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
DIAGRAMS_SRC = PROJECT_ROOT / "diagrams" / "src"  # Mermaid source files
DIAGRAMS_OUT = PROJECT_ROOT / "diagrams"          # Generated output
TERMS_FILE = PROJECT_ROOT / "_terms.yml"

# PNG variants: (suffix, width in pixels)
# Only @4x for print; web uses SVG
PNG_VARIANTS = [
    ("@4x", 3200),   # diagram@4x.png (print 300 DPI)
]


def get_artifact_paths(stem: str) -> list[Path]:
    """Return all artifact paths for a diagram stem (svg + png variants)"""
    paths = [DIAGRAMS_OUT / f"{stem}.svg"]
    for suffix, _ in PNG_VARIANTS:
        paths.append(DIAGRAMS_OUT / f"{stem}{suffix}.png")
    return paths


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

    # Strip YAML frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    # Manually preface with ELK renderer init block
    elk_init = '%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%\n'
    if not content.strip().startswith("%%{init"):
        content = elk_init + content

    # Write to temp file and render
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False
    ) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        outputs = []
        for fmt in formats:
            if fmt == "png":
                # Generate multiple PNG variants at different widths
                for suffix, width in PNG_VARIANTS:
                    output_path = output_dir / f"{mmd_path.stem}{suffix}.png"
                    cmd = [
                        "uv", "run", "mmdc",
                        "-i", str(tmp_path),
                        "-o", str(output_path),
                        "-e", "png",
                        "-q",
                        "-w", str(width),
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        print(f"  Error rendering {mmd_path.name} to {output_path.name}: {result.stderr}")
                        return False
                    outputs.append(output_path.name)
            else:
                # SVG (no scale needed)
                output_path = output_dir / f"{mmd_path.stem}.{fmt}"
                cmd = [
                    "uv", "run", "mmdc",
                    "-i", str(tmp_path),
                    "-o", str(output_path),
                    "-e", fmt,
                    "-q",
                ]
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
    if not DIAGRAMS_SRC.exists():
        print(f"Error: {DIAGRAMS_SRC} directory not found")
        return 1

    init_block = load_mermaid_init()

    # Find .mmd files
    if patterns:
        mmd_files = []
        for pattern in patterns:
            # Check if it's a path (absolute or relative)
            path = Path(pattern)
            if path.is_absolute() or pattern.startswith(("./", "../")) or "/" in pattern:
                # Treat as file path
                if path.exists() and path.suffix == ".mmd":
                    mmd_files.append(path.resolve())
                elif not path.suffix:
                    # Try adding .mmd extension
                    path_with_ext = Path(f"{pattern}.mmd")
                    if path_with_ext.exists():
                        mmd_files.append(path_with_ext.resolve())
            else:
                # Treat as diagram name for globbing in DIAGRAMS_SRC
                if not pattern.endswith(".mmd"):
                    pattern = f"{pattern}.mmd"
                matches = list(DIAGRAMS_SRC.glob(pattern))
                mmd_files.extend(matches)
    else:
        mmd_files = list(DIAGRAMS_SRC.glob("*.mmd"))

    if not mmd_files:
        print("No .mmd files found to render")
        return 0

    print(f"Rendering {len(mmd_files)} diagram(s) to SVG + PNG (@4x)...")
    success_count = 0
    for mmd_path in sorted(mmd_files):
        if render_diagram(mmd_path, DIAGRAMS_OUT, init_block):
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

        def _handle_render(self, path: Path, event_type: str):
            """Common handler for modified/created events"""
            if path.suffix != ".mmd":
                return

            # Debounce: skip if rendered within last second
            now = time.time()
            if path in self.last_render and now - self.last_render[path] < 1:
                return
            self.last_render[path] = now

            print(f"\n{event_type}: {path.name}")
            render_diagram(path, DIAGRAMS_OUT, init_block)

        def on_modified(self, event):
            if event.is_directory:
                return
            self._handle_render(Path(event.src_path), "Change detected")

        def on_created(self, event):
            if event.is_directory:
                return
            self._handle_render(Path(event.src_path), "New file detected")

        def on_deleted(self, event):
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix != ".mmd":
                return

            print(f"\nFile deleted: {path.name}")
            for artifact in get_artifact_paths(path.stem):
                if artifact.exists():
                    artifact.unlink()
                    print(f"  Removed {artifact.name}")

        def on_moved(self, event):
            if event.is_directory:
                return

            src_path = Path(event.src_path)
            dest_path = Path(event.dest_path)

            # Handle .mmd file moved OUT of watched dir (treat as delete)
            if src_path.suffix == ".mmd" and dest_path.parent != DIAGRAMS_SRC:
                print(f"\nFile moved out: {src_path.name}")
                for artifact in get_artifact_paths(src_path.stem):
                    if artifact.exists():
                        artifact.unlink()
                        print(f"  Removed {artifact.name}")
                return

            # Handle .mmd file moved INTO or WITHIN watched dir
            if dest_path.suffix != ".mmd":
                return
            if dest_path.parent != DIAGRAMS_SRC:
                return

            print(f"\nFile renamed: {src_path.name} -> {dest_path.name}")

            # Rename existing artifacts
            renamed = False
            for old_artifact in get_artifact_paths(src_path.stem):
                if old_artifact.exists():
                    new_name = old_artifact.name.replace(src_path.stem, dest_path.stem)
                    new_artifact = DIAGRAMS_OUT / new_name
                    old_artifact.rename(new_artifact)
                    print(f"  Renamed {old_artifact.name} -> {new_artifact.name}")
                    renamed = True

            # If no artifacts existed, render fresh
            if not renamed:
                render_diagram(dest_path, DIAGRAMS_OUT, init_block)

    if not DIAGRAMS_SRC.exists():
        print(f"Error: {DIAGRAMS_SRC} directory not found")
        sys.exit(1)

    # Initial render
    print("Initial render...")
    render_all()

    # Start watching
    print(f"\nWatching {DIAGRAMS_SRC} for changes... (Ctrl+C to stop)")
    observer = Observer()
    observer.schedule(MermaidHandler(), str(DIAGRAMS_SRC), recursive=False)
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
