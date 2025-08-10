
#!/usr/bin/env python3
"""
sizing.py  –  Complete COCOMO II v2.1 Sizing Utilities
======================================================

Implements everything in Section 2 of the Model Definition Manual:
 • Function‑Point counting with automatic complexity classification
 • UFP‑to‑SLOC conversion (Table 4, incl. USR_1…USR_5 slots)
 • Equivalent‑SLOC aggregation of New + Adapted code
 • Requirements Evolution & Volatility (REVL) adjustment (Eq. 5)

Author : Aayush Gid  |  Licence : MIT
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# 0.  Function‑Point plumbing
# ----------------------------------------------------------------------

class FPType(Enum):
    ILF = "ILF"   # Internal Logical File
    EIF = "EIF"   # External Interface File
    EI  = "EI"    # External Input
    EO  = "EO"    # External Output
    EQ  = "EQ"    # External Inquiry


# --- Complexity decision tables (Table 2) ------------------------------
# Each entry : (DET_range, FTR/RET_range) ➜ complexity string

# Helper ranges
def _r(low, hi):  # inclusive range helper
    return range(low, hi + 1)

# ILF / EIF use RET vs DET
_ILF_EIF_RULES = {
    # RET 1
    (_r(1, 1), _r(1, 19))       : "Low",
    (_r(1, 1), _r(20, 50))      : "Low",
    (_r(1, 1), _r(51, 1_000_000)): "Average",
    # RET 2‑5
    (_r(2, 5), _r(1, 19))       : "Low",
    (_r(2, 5), _r(20, 50))      : "Average",
    (_r(2, 5), _r(51, 1_000_000)): "High",
    # RET ≥6
    (_r(6, 1_000_000), _r(1, 19))  : "Average",
    (_r(6, 1_000_000), _r(20, 50)) : "High",
    (_r(6, 1_000_000), _r(51, 1_000_000)) : "High",
}

# EO / EQ use FTR vs DET  (same thresholds)
_EO_EQ_RULES = {
    (_r(0, 1), _r(1, 5))       : "Low",
    (_r(0, 1), _r(6, 19))      : "Low",
    (_r(0, 1), _r(20, 1_000_000)): "Average",
    (_r(2, 3), _r(1, 5))       : "Low",
    (_r(2, 3), _r(6, 19))      : "Average",
    (_r(2, 3), _r(20, 1_000_000)): "High",
    (_r(4, 1_000_000), _r(1, 5))  : "Average",
    (_r(4, 1_000_000), _r(6, 19)) : "High",
    (_r(4, 1_000_000), _r(20, 1_000_000)): "High",
}

# EI uses different DET thresholds
_EI_RULES = {
    (_r(0, 1), _r(1, 4))       : "Low",
    (_r(0, 1), _r(5, 15))      : "Low",
    (_r(0, 1), _r(16, 1_000_000)): "Average",
    (_r(2, 3), _r(1, 4))       : "Low",
    (_r(2, 3), _r(5, 15))      : "Average",
    (_r(2, 3), _r(16, 1_000_000)): "High",
    (_r(3, 1_000_000), _r(1, 4))  : "Average",
    (_r(3, 1_000_000), _r(5, 15)) : "High",
    (_r(3, 1_000_000), _r(16, 1_000_000)): "High",
}

# Map type → its rule dict
_RULE_MAP = {
    FPType.ILF: _ILF_EIF_RULES,
    FPType.EIF: _ILF_EIF_RULES,
    FPType.EO : _EO_EQ_RULES,
    FPType.EQ : _EO_EQ_RULES,
    FPType.EI : _EI_RULES,
}

# Complexity weights (Table 3)
_WEIGHTS = {
    FPType.ILF:  {"Low": 7, "Average": 10, "High": 15},
    FPType.EIF:  {"Low": 5, "Average": 7,  "High": 10},
    FPType.EI :  {"Low": 3, "Average": 4,  "High": 6},
    FPType.EO :  {"Low": 4, "Average": 5,  "High": 7},
    FPType.EQ :  {"Low": 3, "Average": 4,  "High": 6},
}

# ----------------------------------------------------------------------
# 1.  Language back‑firing ratios (Table 4)
# ----------------------------------------------------------------------
UFP_TO_SLOC: Dict[str, int] = {
    # Language           : SLOC per UFP
    "Access": 38, "Ada 83": 83, "Ada 95": 49, "AI Shell": 49,
    "APL": 32, "Assembly - Basic": 320, "Assembly - Macro": 213,
    "Basic - ANSI": 64, "Basic - Compiled": 91, "Basic - Visual": 32,
    "C": 128, "C++": 55, "Cobol (ANSI 85)": 91, "Database – Default": 40,
    "Fifth Generation Language": 4, "First Generation Language": 320,
    "Forth": 64, "Fortran 77": 107, "Fortran 95": 71,
    "Fourth Generation Language": 20, "High Level Language": 64,
    "HTML 3.0": 15, "Java": 53, "Jovial": 107, "Lisp": 64,
    "Machine Code": 640, "Modula 2": 80, "Pascal": 91, "PERL": 27,
    "PowerBuilder": 16, "Prolog": 64, "Python:": 29,"Query – Default": 13,
    "Report Generator": 80, "Second Generation Language": 107,
    "Simulation – Default": 46, "Spreadsheet": 6,
    "Third Generation Language": 80, "Unix Shell Scripts": 107,
    "USR_1": 1, "USR_2": 1, "USR_3": 1, "USR_4": 1, "USR_5": 1,
    "Visual Basic 5.0": 29, "Visual C++": 34,
}
# alias dictionary keys to allow lower‑case access
UFP_TO_SLOC = {k.lower(): v for k, v in UFP_TO_SLOC.items()}

# ----------------------------------------------------------------------
# 2.  Core dataclasses
# ----------------------------------------------------------------------

@dataclass
class FPCount:
    """Represents one *instance* of a Function‑Point element before weighting."""
    fp_type: FPType
    det: int                    # Data Element Types
    ftr_or_ret: int             # FTR for EI/EO/EQ,  RET for ILF/EIF


@dataclass
class SizingResult:
    """Holds final sizing outputs."""
    ufp: float
    sloc: float
    sloc_after_revl: float


# ----------------------------------------------------------------------
# 3.  Complexity / weighting helpers
# ----------------------------------------------------------------------

def _determine_complexity(item: FPCount) -> str:
    """Return 'Low' / 'Average' / 'High' using Table 2 rules."""
    rules = _RULE_MAP[item.fp_type]
    for ftr_range, det_range in rules:
        if item.ftr_or_ret in ftr_range and item.det in det_range:
            return rules[(ftr_range, det_range)]
    raise ValueError(f"No rule for {item}")

def weight_fp_items(items: List[FPCount]) -> int:
    """Compute UFP from a list of raw FP items."""
    total = 0
    for it in items:
        complexity = _determine_complexity(it)
        weight = _WEIGHTS[it.fp_type][complexity]
        total += weight
    return total


# ----------------------------------------------------------------------
# 4.  UFP → SLOC conversion
# ----------------------------------------------------------------------

def ufp_to_sloc(ufp: float, language: str) -> float:
    """Convert Unadjusted FP to SLOC via Table 4 ratio."""
    ratio = UFP_TO_SLOC.get(language.lower())
    if ratio is None:
        raise KeyError(f"Language '{language}' not found in Table 4.")
    return ufp * ratio


# ----------------------------------------------------------------------
# 5.  REVL adjustment (Eq. 5)
# ----------------------------------------------------------------------

def apply_revl(size_delivered: float, revl_percent: float) -> float:
    """
    Apply Requirements Evolution & Volatility:

        Size_effective = Size_delivered × (1 + REVL/100)
    """
    return size_delivered * (1.0 + revl_percent / 100.0)


# ----------------------------------------------------------------------
# 6.  Aggregate sizing API
# ----------------------------------------------------------------------

def compute_size(
    new_sloc: float,
    adapted_esloc: float = 0.0,
    revl_percent: float = 0.0,
) -> SizingResult:
    """
    Aggregate New + Adapted ESLOC, then apply REVL.

    • `adapted_esloc` should come from reuse.calc_esloc()
    • Reused/COTS *unmodified* SLOC are **not counted** here.
    """
    delivered = new_sloc + adapted_esloc
    effective = apply_revl(delivered, revl_percent)
    return SizingResult(ufp=0.0, sloc=delivered, sloc_after_revl=effective)


# ----------------------------------------------------------------------
# 7.  Quick demo
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Illustrative FP list (very small example)
    fp_items = [
        FPCount(FPType.ILF, det=25, ftr_or_ret=3),   # Average → 10
        FPCount(FPType.EI,  det=10, ftr_or_ret=2),   # Average → 4
        FPCount(FPType.EO,  det=22, ftr_or_ret=4),   # High    → 7
    ]
    ufp = weight_fp_items(fp_items)
    sloc = ufp_to_sloc(ufp, "Java")
    res = compute_size(new_sloc=sloc, adapted_esloc=0, revl_percent=15)

    print(f"UFP total           : {ufp}")
    print(f"SLOC (Java)         : {sloc:,.0f}")
    print(f"SLOC after 15% REVL : {res.sloc_after_revl:,.0f}")
