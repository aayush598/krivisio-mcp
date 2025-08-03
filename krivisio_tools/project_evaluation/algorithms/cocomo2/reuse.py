#!/usr/bin/env python3
"""
reuse.py  –  COCOMO II.2000 Reuse / Adaptation Sizing Model
==================================================================
Converts Adapted Source Lines Of Code (ASLOC) into Equivalent SLOC
(ESLOC) and, when automatic translation is used, estimates PM_auto.

References (COCOMO II v2.1 manual)
----------------------------------
• Eq. 4  : Adaptation Adjustment Modifier (AAM) :contentReference[oaicite:0]{index=0}
• Table 5: Software Understanding (SU) rating values         :contentReference[oaicite:1]{index=1}
• Table 6: Assessment & Assimilation (AA) increments         :contentReference[oaicite:2]{index=2}
• Table 7: Programmer Unfamiliarity (UNFM) multipliers       :contentReference[oaicite:3]{index=3}
"""

from __future__ import annotations
from dataclasses import dataclass


# ──────────────────────────────────────────────────────────────────────────
# Rating dictionaries (verbatim from Tables 5‑7)

SU_VALUES = {  # Software‑understanding penalty (%)
    "VH": 10, "H": 20, "N": 30, "L": 40, "VL": 50,
}

AA_VALUES = {  # Assessment & Assimilation increment (%)
    "0": 0, "2": 2, "4": 4, "6": 6, "8": 8,  # allow string codes
    0: 0, 2: 2, 4: 4, 6: 6, 8: 8,            # …or numeric keys
}

UNFM_VALUES = {  # Programmer unfamiliarity multiplier
    "CF": 0.0,  # Completely familiar
    "MF": 0.2,  # Mostly familiar
    "SF": 0.4,  # Somewhat familiar
    "CFa": 0.6, # Considerably familiar
    "MU": 0.8,  # Mostly unfamiliar
    "CU": 1.0,  # Completely unfamiliar
}

# Default productivity for automatic translation (SLOC / PM)
ATPROD_DEFAULT = 2400  # :contentReference[oaicite:4]{index=4}


# ──────────────────────────────────────────────────────────────────────────
# Helper dataclass for reuse parameters

@dataclass
class ReuseParams:
    """All inputs needed for the COCOMO II reuse calculation."""
    asloc: float               # Adapted SLOC
    dm: float                  # % design modified   (0‑100+)
    cm: float                  # % code modified     (0‑100+)
    im: float                  # % integration effort (0‑100+)
    su: float                  # Software understanding increment (%)
    unfm: float                # Unfamiliarity multiplier (0.0‑1.0)
    aa: float                  # Assessment & assimilation increment (%)
    at: float = 0.0            # % automatically translated (0‑100)
    atprod: float = ATPROD_DEFAULT  # translation prod. (SLOC/PM)

    def __post_init__(self):
        # quick validity checks
        for name in ("dm", "cm", "im", "su", "aa", "at"):
            val = getattr(self, name)
            if val < 0:
                raise ValueError(f"{name.upper()} must be ≥ 0 (got {val})")
        if self.asloc <= 0:
            raise ValueError("ASLOC must be positive")


# ──────────────────────────────────────────────────────────────────────────
# Core model functions

def calc_aaf(dm: float, cm: float, im: float) -> float:
    """
    Adaptation Adjustment Factor – linear mix of DM, CM, IM.

        AAF = 0.4·DM + 0.3·CM + 0.3·IM          (Eq. 4, first line)
    """
    return 0.4 * dm + 0.3 * cm + 0.3 * im


def calc_aam(aaf: float, su: float, unfm: float, aa: float) -> float:
    """
    Adaptation Adjustment Modifier – nonlinear reuse multiplier.

    Piece‑wise definition (Eq. 4):

      • If AAF ≤ 50:
          AAM = AA + (SU · UNFM · AAF) / 100
      • If AAF > 50:
          AAM = AA + SU·UNFM + SU·UNFM·0.02·(AAF − 50)

    All symbols are *percentages* except UNFM (0..1).
    """
    if aaf <= 50:
        return aa + (su * unfm * aaf) / 100.0
    # extra “steeper‑than‑linear” penalty for large modifications
    return aa + su * unfm + su * unfm * 0.02 * (aaf - 50)


def calc_esloc(params: ReuseParams) -> float:
    """
    Compute Equivalent SLOC (ESLOC) for adapted code:

        ESLOC = ASLOC × [ (1 − AT/100)  +  (AT/100)·AAM ]

    This backs out the auto‑translated portion, replaces it with its
    AAM‑weighted equivalent, and leaves un‑translated lines unchanged.
    """
    aaf = calc_aaf(params.dm, params.cm, params.im)
    aam = calc_aam(aaf, params.su, params.unfm, params.aa)
    return params.asloc * ((1.0 - params.at / 100.0) + (params.at / 100.0) * aam)


def calc_pm_auto(params: ReuseParams) -> float:
    """
    PM_auto – Person‑Months consumed purely by automatic translation
    (Eq. 6):

        PM_auto = (AT/100) · ASLOC / ATPROD
    """
    return (params.at / 100.0) * params.asloc / params.atprod


# ──────────────────────────────────────────────────────────────────────────
# Convenience helpers for rating‑code → numeric lookup

def su_from_rating(rating: str) -> float:
    """Convert SU rating code ('VH','H',…) to % value."""
    try:
        return SU_VALUES[rating.upper()]
    except KeyError:
        raise ValueError(f"Unknown SU rating '{rating}'")


def aa_from_rating(code) -> float:
    """Convert AA code (0,2,4,6,8 or strings) to % value."""
    try:
        return AA_VALUES[code]
    except KeyError:
        raise ValueError(f"Unknown AA increment '{code}'")


def unfm_from_rating(code: str) -> float:
    """Convert UNFM mnemonic ('CF','SF',…) to multiplier."""
    try:
        return UNFM_VALUES[code.upper()]
    except KeyError:
        raise ValueError(f"Unknown UNFM rating '{code}'")


# ──────────────────────────────────────────────────────────────────────────
# Example (run `python reuse.py` to test quickly)
if __name__ == "__main__":
    # Sample: 30 KSLOC adapted, 20 %DM, 30 %CM, 40 %IM,
    #          SU = 30 % (Nominal), UNFM = 0.4 (Somewhat familiar),
    #          AA = 2 %,  AT = 25 %.
    p = ReuseParams(
        asloc=30_000,
        dm=20, cm=30, im=40,
        su=su_from_rating("N"),
        unfm=unfm_from_rating("SF"),
        aa=aa_from_rating(2),
        at=25,
    )
    esloc = calc_esloc(p)
    pm_auto = calc_pm_auto(p)
    print(f"Equivalent SLOC : {esloc:,.0f}")
    print(f"PM_auto (translation only): {pm_auto:.2f}")
