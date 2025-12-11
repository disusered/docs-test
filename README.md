# XBOL Technical Documentation

Technical documentation for the XBOL system, built with [Jupyter Book](https://jupyterbook.org/) and [MyST Markdown](https://mystmd.org/).

## Quick Start

```bash
# Install dependencies
uv sync

# Start development server (live reload)
uv run jupyter-book start

# Build the site
uv run jupyter-book build
```

The site will be available at `http://localhost:3000` when using `start`.

## Project Structure

```
content/
index.md              # Landing page
glossary.md           # Central glossary
_template.md          # Template for new documents
architecture/         # Architecture documentation
appendices/           # Supplementary material
```

## Adding Content

1. Copy `content/_template.md` to the appropriate directory
2. Update the frontmatter (title, author)
3. Write your content
4. Documents are auto-included in the table of contents

### Mermaid Diagrams

Use literal include to add an external mermaid diagram:

```markdown
```{literalinclude} /path/to/your/diagram.mmd
  :language: mermaid
```
```

Use the standard theme for consistent styling:

````markdown
```{mermaid}
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#2563eb',
  'primaryTextColor': '#ffffff',
  'primaryBorderColor': '#1d4ed8',
  'secondaryColor': '#7c3aed',
  'tertiaryColor': '#f1f5f9',
  'lineColor': '#64748b',
  'textColor': '#1e293b'
}}}%%
flowchart LR
  A[Component] --> B[Component]
`````

### Glossary Terms

Add terms to `content/glossary.md`:

```markdown
TermName
: Definition of the term.
```

Reference in other documents: `` {term}`TermName` ``

### Cross-References

- Link to page: `` {doc}`./path/to/file` ``
- Link to term: `` {term}`TermName` ``
- Link to section: `` {ref}`section-label` ``

## Terminology & Colors

See `_terms.yml` for:

- **Reviewable terms**: Central reference for terms that may change during review
- **Color palette**: Consistent colors for diagrams and styling

For bulk terminology changes, use find/replace across the `content/` directory.

## Build Outputs

```bash
uv run jupyter-book build              # Default site
uv run jupyter-book build --pdf        # PDF output
uv run jupyter-book build --html       # Static HTML
uv run jupyter-book build --all        # All formats

uv run jupyter-book clean              # Clean build artifacts
```

Build output goes to `_build/` (gitignored).

## Configuration

| File                 | Purpose                                       |
| -------------------- | --------------------------------------------- |
| `myst.yml`           | Project metadata, TOC structure, site options |
| `_terms.yml`         | Reviewable terminology, color palette         |
| `_static/custom.css` | Custom site styling                           |

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

# TODO

- [x] Hide author in documents
- [x] Hide edit/github button in documents
- [ ] Mermaid background color vis a vis dark mode
- [ ] Mermaid zoom/open in new tab
- [ ] Glossary terms
  - [ ] Gateway
  - [ ] Payments
  - [ ] Notifications
  - [ ] Ticketing
  - [ ] Identity
- [ ] Github Actions publish to pages <https://jupyterbook.org/stable/get-started/publish/>
- [ ] Export to PDF
