# XBOL Technical Documentation

Technical documentation for the XBOL system, built with [Jupyter Book](https://jupyterbook.org/) and [MyST Markdown](https://mystmd.org/).

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)

## Quick Start

```bash
uv sync                        # Install dependencies
uv run jupyter-book start      # Dev server at localhost:3000
uv run jupyter-book build      # Build site
uv run render-diagrams         # Render all diagrams
```

## Exporting to PDF

### Prerequisites

Install [Typst](https://typst.app/) for PDF generation:

```bash
# macOS
brew install typst

# Linux (Arch)
pacman -S typst

# Linux (cargo)
cargo install typst-cli

# Windows
winget install --id Typst.Typst
```

### Build Exports

```bash
uv run jupyter-book build --typst   # Build PDF (via Typst)
uv run jupyter-book build --all     # Build all exports
```

Outputs are saved to `exports/`.

**Note**: DOCX export is not supported for multi-article books. Individual pages can be exported to DOCX using page-level export configuration.

## Adding Content

1. Copy `content/_template.md` to `content/architecture/` or `content/appendices/`
2. Update frontmatter and write content
3. Documents auto-appear in table of contents

See the template for MyST syntax examples (cross-references, admonitions, tables).

## Diagrams

Diagrams live in `diagrams/` as `.mmd` files and are rendered to themed SVGs.

### Setup (one-time)

```bash
uv sync --extra diagrams
uv run playwright install chromium
```

### Workflow

```bash
uv run render-diagrams              # Render all diagrams
uv run render-diagrams --watch      # Watch mode for editing
uv run render-diagrams context      # Render specific diagram
```

### Creating a diagram

1. Create `diagrams/mydiagram.mmd`:

   ```mermaid
   flowchart LR
     A[Service A] --> B[Service B]
     B --> C[Database]
   ```

2. Render: `uv run render-diagrams mydiagram`

3. Reference in markdown:

   ````markdown
   ```{figure} /diagrams/mydiagram.svg
   :name: fig-mydiagram
   :width: 100%

   Caption text - [View full size](/diagrams/mydiagram.svg)
   ```
   ````

   ```

   ```

Theme is auto-injected from `_terms.yml`. Commit both `.mmd` and `.svg` files.

## Configuration

| File                 | Purpose                              |
| -------------------- | ------------------------------------ |
| `myst.yml`           | Project metadata, TOC, site options  |
| `_terms.yml`         | Terminology reference, diagram theme |
| `_static/custom.css` | Custom styling                       |
