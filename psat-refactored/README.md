# PSAT - Power System Analysis Toolbox (Refactored Python Port)

This directory contains a refactored Python version of PSAT,
converted from the original MATLAB source (third-party/psat/).

## Structure

```
psat/
├── __init__.py          # Top-level package
├── pyproject.toml
├── core/                # Core PSAT modules (solver, settings, etc.)
├── cli/                 # Command-line tools
├── gui/                 # GUI-related modules
├── solvers/             # Low-level solvers (zbuild, etc.)
├── gams/                # GAMS interface
├── packages/            # PSAT component classes (renamed from @class)
│   ├── buclass/         # Bus class
│   ├── pqclass/         # PQ load class
│   ├── pvclass/         # PV generator class
│   ├── lnclass/         # Line class
│   └── ...              # ~57 component classes
└── filters/             # Filter modules
```

## Usage

```python
import psat
from psat.packages import buclass
```
