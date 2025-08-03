
#!/usr/bin/env python3
"""
schedule.py  –  COCOMO II v2.1 Schedule Estimation
==================================================

Implements Equation 14 and Table 34 of the Model Definition Manual:

    • Nominal schedule:
          TDEV_NS = C · (PM_NS)^( D + 0.2·(E − B) )

    • Final schedule:
          TDEV = TDEV_NS · SCED%

    where  SCED% = 0.75, 0.85, 1.00, 1.30, 1.60  for VL, L, N, H, VH.

If the supplied Person‑Months already *include* the SCED effort‑multiplier
(e.g. 1.43 for VL) the `calculate_schedule` helper will back it out so the
formula is always applied to **PM_NS** as required by the manual.

All numeric values come verbatim from the calibration constants and tables
in the COCOMO II v2.1 documentation.

Author : Aayush Gid  |  Licence : MIT
"""

from math import pow
from typing import Literal

# ──────────────────────────────────────────────────────────────────────────
# Constants (Table 62 and text)  :contentReference[oaicite:2]{index=2}
C = 3.67     # Schedule coefficient
D = 0.28     # Schedule base exponent
B = 0.91     # Effort‑scaling intercept (needed for exponent term)

# ──────────────────────────────────────────────────────────────────────────
# SCED tables (Table 34)  :contentReference[oaicite:3]{index=3}
SCED_PERCENT = {      # schedule stretch / compression factors
    "VL": 0.75,       # 75 % of nominal schedule
    "L":  0.85,       # 85 %
    "N":  1.00,       # 100 %
    "H":  1.30,       # 130 %
    "VH": 1.60,       # 160 %
}

SCED_EFFORT_EM = {    # effort multipliers for *effort* calc (Table 62)
    "VL": 1.43,
    "L":  1.14,
    "N":  1.00,
    "H":  1.00,
    "VH": 1.00,
}

Rating = Literal["VL", "L", "N", "H", "VH"]

# ──────────────────────────────────────────────────────────────────────────
# Core helpers
# ──────────────────────────────────────────────────────────────────────────

def nominal_tdev(pm_ns: float, E: float) -> float:
    """
    Compute **nominal‑schedule** calendar months, *without* SCED effects.

    Parameters
    ----------
    pm_ns : float
        Effort in person‑months **excluding** the SCED effort‑multiplier.
    E : float
        The COCOMO scaling exponent (cf. effort.py::calc_E).

    Returns
    -------
    float : TDEV_NS  (months)
    """
    exponent = D + 0.2 * (E - B)
    return C * pow(pm_ns, exponent)


def calculate_schedule(
    pm: float,
    E: float,
    sced_rating: Rating = "N",
    pm_includes_sced: bool = True,
) -> float:
    """
    Full Time‑to‑Develop (TDEV) in months.

    Parameters
    ----------
    pm : float
        Person‑Months either **with** or **without** the SCED effort‑multiplier.
    E : float
        Effort scaling exponent from scale factors.
    sced_rating : {"VL","L","N","H","VH"}
        Required Development Schedule rating (Table 34).
    pm_includes_sced : bool, default True
        • True  – pm already has SCED EM applied (common case  
                  when you used effort.py with a full EM set).  
        • False – pm is already PM_NS.

    Returns
    -------
    float : Final TDEV (calendar months)
    """
    if sced_rating not in SCED_PERCENT:
        raise ValueError(f"Invalid SCED rating '{sced_rating}'. "
                         f"Choose from {list(SCED_PERCENT)}.")

    # Back‑out SCED effort‑multiplier if necessary
    pm_ns = pm
    if pm_includes_sced:
        em = SCED_EFFORT_EM[sced_rating]
        pm_ns /= em

    tdev_ns = nominal_tdev(pm_ns, E)
    tdev_final = tdev_ns * SCED_PERCENT[sced_rating]
    return tdev_final

# ──────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Example same as Section 1.2 in the manual:
    #   • size 100 KSLOC
    #   • all cost drivers nominal (=> effort 586.61 PM, E=1.15)
    #   • schedule rating Nominal (SCED=N)
    pm_example = 586.61        # includes SCED EM = 1.0 (nominal)
    E_example = 1.15
    tdev = calculate_schedule(pm_example, E_example, "N", pm_includes_sced=True)

    print(f"Estimated Development Time (TDEV): {tdev:.2f} months")
