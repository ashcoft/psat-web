# `psat-converted/` — mechanical MATLAB → Python port of upstream PSAT

This directory contains a **mechanical, best-effort textual conversion** of
every `.m` file in the upstream [ashcoft/PSAT](https://github.com/ashcoft/PSAT)
MATLAB toolbox (vendored as the read-only submodule at
[`third-party/psat/`](../third-party/psat/)).

It is **not** a runnable Python port of PSAT. The files are intended as a
familiar Python-shaped starting point for manual review.

## How it was generated

```bash
python tools/matlab_to_python.py third-party/psat psat-converted
```

The script ([`tools/matlab_to_python.py`](../tools/matlab_to_python.py))
applies these textual transforms to every `.m` file:

| From                          | To                            |
|-------------------------------|-------------------------------|
| `function name(...)`          | `def name(...):`              |
| `function [a, b] = name(...)` | *(left as-is, manual edit)*   |
| `end` (on its own line)       | *(removed — Python uses indents)* |
| `% ...`                       | `# ...` (line and inline)     |
| `&&` / `\|\|`                 | ` and ` / ` or `              |
| `~=`                          | `!=`                          |
| `~x`                          | `not x`                       |
| trailing `;`                  | dropped                       |
| `disp(`                       | `print(`                      |
| `zeros(m, n)`                 | `np.zeros((m, n))`            |
| `ones(m, n)`                  | `np.ones((m, n))`             |
| `eye(n)`                      | `np.eye(n)`                   |
| `length(`                     | `len(`                        |
| `inv(` / `eig(` / `norm(`     | `np.linalg.inv(` / `eig(` / `norm(` |
| `true` / `false`              | `True` / `False`              |
| `Inf` / `NaN`                 | `np.inf` / `np.nan`           |
| `pi` (whole word)             | `np.pi`                       |
| `for i = 1:n`                 | `for i in range(1, n+1):`     |

If a converted file ends up using `np.*` or `scipy.sparse`, the converter
prepends the corresponding `import` line.

## What is NOT converted

A faithful Python port of PSAT is a large project. The converter is
intentionally minimal; the following MATLAB constructs are *not* handled and
will require manual rework:

- **Multi-output signatures** `function [a, b] = name(...)` are left as-is
  (the function name is not extracted; you must hand-edit them to Python
  `def name(...)` + tuple return).
- **MATLAB struct / classdef / methods** are not translated.
- **MATLAB indexing/slicing** (e.g. `A(1:n, :)`, `x{1}`, struct field access
  `s.field`, dynamic field names via `(name)`) is left untouched.
- **Matrix arithmetic semantics**: `*` and `/` in MATLAB are matrix ops by
  default; the converter does not insert `.dot()` / `@` / `np.matmul`.
- **Cell arrays**, `containers.Map`, `function handles` (`@foo`).
- **`global` / `persistent` / `nargin` / `varargin` / `varargout`** still
  appear in the converted text and have no Python equivalent.
- **GUIs** (`fm_*fig.m`, `fm_*.m` that use `figure` / `uicontrol` /
  `set(gcf, ...)`) are obviously not Python-portable; the converted files
  are just textual references.
- **Errors, warnings, `try/catch`** keep their MATLAB spelling and need to be
  ported to `raise` / `warnings.warn` / `try/except`.

## Layout

The directory tree mirrors the upstream `third-party/psat/` layout one-to-one.
Each `.m` file `third-party/psat/<rel>` becomes a corresponding
`psat-converted/<rel>.py`. Original source paths are recorded in the
`# Source: third-party/psat/<rel>.m` banner at the top of every converted
file.

## How to refresh after upstream changes

```bash
# pull the latest upstream MATLAB code
git submodule update --remote third-party/psat

# re-run the converter (this overwrites psat-converted/ in place)
rm -rf psat-converted
python tools/matlab_to_python.py third-party/psat psat-converted
```

## License

The upstream PSAT is © Federico Milano, distributed under **GPL-2.0+**.
The mechanical conversion in this directory is therefore also under
GPL-2.0+. See [`third-party/psat/gnulicense.txt`](../third-party/psat/gnulicense.txt)
for the full text.
