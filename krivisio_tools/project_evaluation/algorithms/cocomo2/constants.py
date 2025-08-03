
"""
COCOMO II.2000 constants and rating scales

Source:
- COCOMO II.2000 Model Definition Manual (v2.1)
- Pages 73–75: Scale Factors, Effort Multipliers, Default Ratings

These constants are used across all estimation steps in the COCOMO II Post-Architecture model.
"""

from typing import Dict


# ----------------------------------------
# Base Constants
# ----------------------------------------

A: float = 2.94  # Effort coefficient
B: float = 0.91  # Exponent coefficient (KSLOC^E)
C: float = 3.67  # Schedule coefficient
D: float = 0.28  # Schedule exponent


# ----------------------------------------
# Scale Factors (SFs)
# ----------------------------------------

SCALE_FACTORS: Dict[str, Dict[str, float]] = {
    'PREC': {'VL': 6.20, 'L': 4.96, 'N': 3.72, 'H': 2.48, 'VH': 1.24, 'XH': 0.00},
    'FLEX': {'VL': 5.07, 'L': 4.05, 'N': 3.04, 'H': 2.03, 'VH': 1.01, 'XH': 0.00},
    'RESL': {'VL': 7.07, 'L': 5.65, 'N': 4.24, 'H': 2.83, 'VH': 1.41, 'XH': 0.00},
    'TEAM': {'VL': 5.48, 'L': 4.38, 'N': 3.29, 'H': 2.19, 'VH': 1.10, 'XH': 0.00},
    'PMAT': {'VL': 7.80, 'L': 6.24, 'N': 4.68, 'H': 3.12, 'VH': 1.56, 'XH': 0.00}
}


# ----------------------------------------
# Effort Multipliers (EMs)
# ----------------------------------------

EFFORT_MULTIPLIERS: Dict[str, Dict[str, float]] = {
    'RELY': {'VL': 0.82, 'L': 0.92, 'N': 1.00, 'H': 1.10, 'VH': 1.26},
    'DATA': {'L': 0.90, 'N': 1.00, 'H': 1.14, 'VH': 1.28},
    'CPLX': {'VL': 0.73, 'L': 0.87, 'N': 1.00, 'H': 1.17, 'VH': 1.34, 'XH': 1.74},
    'RUSE': {'L': 0.95, 'N': 1.00, 'H': 1.07, 'VH': 1.15, 'XH': 1.24},
    'DOCU': {'VL': 0.81, 'L': 0.91, 'N': 1.00, 'H': 1.11, 'VH': 1.23},
    'TIME': {'N': 1.00, 'H': 1.11, 'VH': 1.29, 'XH': 1.63},
    'STOR': {'N': 1.00, 'H': 1.05, 'VH': 1.17, 'XH': 1.46},
    'PVOL': {'L': 0.87, 'N': 1.00, 'H': 1.15, 'VH': 1.30},
    'ACAP': {'VL': 1.42, 'L': 1.19, 'N': 1.00, 'H': 0.85, 'VH': 0.71},
    'PCAP': {'VL': 1.34, 'L': 1.15, 'N': 1.00, 'H': 0.88, 'VH': 0.76},
    'PCON': {'VL': 1.29, 'L': 1.12, 'N': 1.00, 'H': 0.90, 'VH': 0.81},
    'APEX': {'VL': 1.22, 'L': 1.10, 'N': 1.00, 'H': 0.88, 'VH': 0.81},
    'PLEX': {'VL': 1.19, 'L': 1.09, 'N': 1.00, 'H': 0.91, 'VH': 0.85},
    'LTEX': {'VL': 1.20, 'L': 1.09, 'N': 1.00, 'H': 0.91, 'VH': 0.84},
    'TOOL': {'VL': 1.17, 'L': 1.09, 'N': 1.00, 'H': 0.90, 'VH': 0.78},
    'SITE': {'VL': 1.22, 'L': 1.09, 'N': 1.00, 'H': 0.93, 'VH': 0.86, 'XH': 0.80},
    'SCED': {'VL': 1.43, 'L': 1.14, 'N': 1.00, 'H': 1.00, 'VH': 1.00}
}


# ----------------------------------------
# UFP to SLOC Conversion Factors
# ----------------------------------------

UFP_TO_SLOC: Dict[str, int] = {
    'Ada 95': 49,
    'C': 128,
    'C++': 55,
    'Java': 53,
    'Python': 29,
    'JavaScript': 53,
    'COBOL': 91
}


# ----------------------------------------
# Default Ratings (Nominal)
# ----------------------------------------

DEFAULT_EMS: Dict[str, str] = {key: 'N' for key in EFFORT_MULTIPLIERS}
DEFAULT_SFS: Dict[str, str] = {key: 'N' for key in SCALE_FACTORS}
