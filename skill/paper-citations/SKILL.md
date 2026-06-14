---
name: paper-citations
description: Use when implementing or modifying a numerical method, algorithm, or theoretical formulation that is derived from a published paper. Enforces a full bibliographic citation with DOI in the module/function docstring.
---

# Paper Citations in Docstrings

When any code implements, approximates, or follows a published method or algorithm, the responsible docstring must include a full bibliographic citation and a resolvable DOI link.

## When to apply

- Implementing a method, algorithm, formula, or approximation derived from a published paper.
- Porting a theoretical procedure into code (e.g., a solver, transformation, or fitting scheme).
- Adding a new module or function whose logic closely follows a specific publication.
- Updating an existing implementation to follow a different reference.

## Required format

Include a `Reference:` block in the relevant module or function docstring:

```python
"""
Short description of what the code does.

Reference:
    Author, A. (YYYY) "Paper title",
    Journal Name, volume, pages
    DOI: https://doi.org/10.xxxx/xxxxxx
"""
```

## Rules

1. **Cite the primary source**, not a secondary summary or lecture note.
2. **DOI is mandatory**. Use the canonical `https://doi.org/...` form.
3. **Be specific**. Include equation numbers or section references when the implementation closely follows a particular part of the paper.
4. **Keep it in the docstring**, not only in a separate markdown note or commit message.
5. **Update the citation** if the implementation changes to follow a different reference.

## Example

```python
"""
DFT exchange-correlation kernel computation for Time-Dependent DFT.

Reference:
    Laikov, D.N. (1997) "Fast evaluation of density functional
    exchange-correlation terms using the expansion of the electron
    density in auxiliary basis sets", Chem. Phys. Lett. 281, 151-156
    DOI: https://doi.org/10.1016/S0009-2614(97)01206-2
"""
```
