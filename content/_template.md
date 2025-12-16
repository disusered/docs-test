---
title: Document Title
# Uncomment and fill as needed:
# subtitle: Optional subtitle
# authors:
#   - name: Author Name
#     email: author@example.com
# date: 2024-01-01
---

# Document Title

Brief introduction to this document's purpose and scope.

## Overview

High-level description of the topic covered.

## Details

### Subsection

Content goes here.

## Diagrams

Use the standard Mermaid theme for consistency. Copy the init block from `_terms.yml`:

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
  A[Component A] --> B[Component B]
  B --> C[Component C]
```

## Cross-References

Reference other documents:
- Link to page: [](./glossary)
- Link to term: XBOL (see glossary)
- Link to section: {ref}`glossary`

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |

## Admonitions

:::{note}
Important information for the reader.
:::

:::{warning}
Critical information that requires attention.
:::

:::{tip}
Helpful suggestion for the reader.
:::

---

<!--
CONTRIBUTOR NOTES:
- Save new documents to content/architecture/ or content/appendices/
- Use consistent terminology from _terms.yml
- Apply Mermaid theme for all diagrams
- Add terms to glossary.md as needed
-->
