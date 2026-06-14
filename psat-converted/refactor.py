#!/usr/bin/env python3
"""
Refactor psat-converted/ into a proper Python package structure.

Source:   psat-converted/  (flat .py files + @class dirs)
Dest:     psat-refactored/psat/  (proper Python package)
"""
import os
import re
import shutil
import sys
from pathlib import Path

# Use UTF-8 for all file writes
_ENCODING = "utf-8"

def _write_text(path, content):
    """Write text with UTF-8 encoding."""
    path.write_text(content, encoding=_ENCODING)

SRC = Path(__file__).resolve().parent.parent / "psat-converted"
DST = Path(__file__).resolve().parent / "psat"

# ── Class directories to rename ──────────────────────────────────────────
CLASS_DIRS = sorted((d.name for d in SRC.iterdir() if d.is_dir() and d.name.startswith("@")))

# ── Module groupings (flat .py -> subpackage) ─────────────────────────────
CORE_MODULES = [
    "psat", "runpsat", "initpsat", "settings", "Contents", "psatdomain",
    "psatsol", "pgrep", "numjacs", "opfeigen", "pert", "symfault", "psed",
]

CLI_MODULES = ["autorun", "checkjac", "benchmark", "closepsat"]

GUI_MODULES = [
    "fm_main", "fm_about", "fm_author", "fm_license", "fm_warranty",
    "fm_install", "fm_uninstall", "fm_update", "fm_advanced",
    "fm_axesdlg", "fm_bar", "fm_base", "fm_block", "fm_build",
    "fm_busfig", "fm_call", "fm_choice", "fm_clock", "fm_comp",
    "fm_component", "fm_cset", "fm_del", "fm_dir", "fm_dirset",
    "fm_disp", "fm_draw", "fm_dump", "fm_dynidx", "fm_dynlf",
    "fm_eigen", "fm_eigfig", "fm_enter", "fm_equiv", "fm_equivfig",
    "fm_errv", "fm_filenum", "fm_flows", "fm_gams", "fm_gamsfig",
    "fm_genstatus", "fm_getxy", "fm_hist", "fm_idx", "fm_iidx",
    "fm_inout", "fm_input", "fm_int", "fm_iview", "fm_laprint",
    "fm_libfig", "fm_limit", "fm_linedlg", "fm_linelist", "fm_lssest",
    "fm_make", "fm_maskrotate", "fm_mat", "fm_matrx", "fm_mintree",
    "fm_n1cont", "fm_ncomp", "fm_new", "fm_nrlf", "fm_omib", "fm_open",
    "fm_opffig", "fm_opfm", "fm_opfrep", "fm_opfsdr", "fm_out",
    "fm_pareto", "fm_plot", "fm_plotfig", "fm_plotsel", "fm_pmufig",
    "fm_pmuloc", "fm_pmun1", "fm_pmurec", "fm_pmurep", "fm_pmutry",
    "fm_pset", "fm_qlim", "fm_report", "fm_restore", "fm_rmgen",
    "fm_save", "fm_set", "fm_setgy", "fm_setting", "fm_simrep",
    "fm_simsave", "fm_simset", "fm_simtd", "fm_snap", "fm_snb",
    "fm_snbfig", "fm_spantree", "fm_spf", "fm_sset", "fm_stat",
    "fm_status", "fm_strjoin", "fm_text", "fm_theme", "fm_themefig",
    "fm_threed", "fm_tstep", "fm_tviewer", "fm_uwfig", "fm_uwpflow",
    "fm_var", "fm_view", "fm_vlim", "fm_vs", "fm_wcall", "fm_windup",
    "fm_write", "fm_writehtm", "fm_writetex", "fm_writetxt", "fm_writexls",
    "fm_xfirst", "fm_xset", "fm_xy", "fm_abcd", "fm_add", "fm_annealing",
    "fm_atc", "fm_cpf", "fm_cpffig", "fm_inilf", "fm_license",
]

SOLVER_MODULES = ["zbuild", "zbuildpi", "fval", "fvar"]

GAMS_MODULES = ["gams/gams"]

BUILD_MODULE = []


def rename_class_dir():
    """Copy @class -> psat/package/__init__.py + psat/package/{files}"""
    for cd in CLASS_DIRS:
        stem = cd.lstrip("@").lower() + "class"
        dst_dir = DST / "packages" / stem
        dst_dir.mkdir(parents=True, exist_ok=True)
        src_dir = SRC / cd
        for f in sorted(src_dir.iterdir()):
            if f.suffix == ".py":
                shutil.copy2(f, dst_dir / f.name)
        # __init__.py
        mods = [f.stem for f in dst_dir.iterdir() if f.suffix == ".py" and f.stem != "__init__"]
        init_lines = [f"from psat.packages.{stem} import {m}" for m in sorted(mods)]
        _write_text(dst_dir / "__init__.py", "\n".join(init_lines) + "\n")


def copy_flat_modules():
    """Copy flat .py into appropriate subpackages."""
    groups = {
        "core": CORE_MODULES,
        "cli": CLI_MODULES,
        "gui": GUI_MODULES,
        "solvers": SOLVER_MODULES,
        "build": BUILD_MODULE,
    }
    for group, mods in groups.items():
        dst_dir = DST / group
        dst_dir.mkdir(parents=True, exist_ok=True)
        imports = []
        for m in mods:
            src_file = SRC / f"{m}.py"
            if src_file.exists():
                shutil.copy2(src_file, dst_dir / f"{m}.py")
                imports.append(f"from psat.{group} import {m}")
        _write_text(dst_dir / "__init__.py", "\n".join(imports) + "\n")


def copy_gams():
    """Copy gams/ subdirectory"""
    gams_src = SRC / "gams"
    if gams_src.is_dir():
        dst_dir = DST / "gams"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(gams_src.iterdir()):
            if f.suffix == ".py":
                shutil.copy2(f, dst_dir / f.name)
        _write_text(dst_dir / "__init__.py", "# GAMS module\n")


def copy_tests():
    """Copy tests/ subdirectory"""
    tests_src = SRC / "tests"
    if tests_src.is_dir():
        dst_dir = DST.parent / "tests"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(tests_src.iterdir()):
            if f.suffix == ".py":
                shutil.copy2(f, dst_dir / f.name)
        _write_text(dst_dir / "__init__.py", "# PSAT test cases\n")


def rewrite_imports():
    """Fix import paths in all copied .py files."""
    for pyfile in DST.rglob("*.py"):
        if pyfile.name == "__init__.py":
            continue
        text = pyfile.read_text(encoding="utf-8", errors="replace")
        orig = text
        
        # Remove banner comments
        lines = text.splitlines()
        lines = [l for l in lines if not l.startswith("# AUTO-CONVERTED") and not l.startswith("# Source:")]
        # Remove blank lines after header
        while lines and lines[0].strip() == "":
            lines.pop(0)
        
        # Add relative import hint instead
        rel = pyfile.relative_to(DST)
        banner = f"# Module: psat.{rel.with_suffix('').as_posix().replace('/', '.')}\n"
        banner += "# Refactored from psat-converted\n"
        text = banner + "\n".join(lines)
        
        if text != orig:
            _write_text(pyfile, text)


def create_pyproject():
    """Create pyproject.toml for the refactored package."""
    content = """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "psat"
version = "2.0"
description = "Refactored Python port of PSAT (Power System Analysis Toolbox)"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "GPL-3.0-or-later" }
dependencies = [
    "numpy>=1.24",
    "scipy>=1.10",
]

[tool.setuptools.packages.find]
include = ["psat*"]
"""
    _write_text(DST.parent / "pyproject.toml", content)


def create_readme():
    """Create a README for the refactored package."""
    content = """# PSAT - Power System Analysis Toolbox (Refactored Python Port)

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
"""
    _write_text(DST.parent / "README.md", content)


def create_top_init():
    """Create the top-level __init__.py"""
    lines = [
        "# PSAT - Refactored Python port\n",
        "# See pyproject.toml for metadata\n",
        "",
        "from psat.core import *",
        "from psat.core import psat, runpsat, initpsat",
        "",
        "__version__ = \"2.0\"\n",
    ]
    _write_text(DST / "__init__.py", "\n".join(lines))


def copy_filters():
    """Copy filters/ if it exists"""
    filt_src = SRC / "filters"
    if filt_src.is_dir():
        dst_dir = DST / "filters"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(filt_src.iterdir()):
            if f.suffix == ".py":
                shutil.copy2(f, dst_dir / f.name)
        _write_text(dst_dir / "__init__.py", "# Filters module\n")


def main():
    print(f"Refactoring {SRC} -> {DST}")
    
    # Clean destination
    if DST.exists():
        shutil.rmtree(DST)
    
    # Create structure
    rename_class_dir()
    copy_flat_modules()
    copy_gams()
    copy_filters()
    copy_tests()
    rewrite_imports()
    create_top_init()
    create_pyproject()
    create_readme()
    
    print(f"Done! {len(list(DST.rglob('*.py')))} Python files in {DST}")


if __name__ == "__main__":
    main()