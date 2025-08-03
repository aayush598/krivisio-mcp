
# cocomo/effort.py
"""
Effort estimation calculations with validation
"""

from krivisio_tools.project_evaluation.algorithms.cocomo2.constants import A, B, SCALE_FACTORS, EFFORT_MULTIPLIERS
import math

class COCOMOIIError(Exception):
    """Custom exception for COCOMO II calculations"""
    pass

def validate_ratings(ems, sfs):
    """Validate that all ratings are valid"""
    errors = []
    
    for factor, rating in sfs.items():
        if factor not in SCALE_FACTORS:
            errors.append(f"Unknown scale factor: {factor}")
        elif rating not in SCALE_FACTORS[factor]:
            errors.append(f"Invalid rating '{rating}' for scale factor {factor}")
    
    for factor, rating in ems.items():
        if factor not in EFFORT_MULTIPLIERS:
            errors.append(f"Unknown effort multiplier: {factor}")
        elif rating not in EFFORT_MULTIPLIERS[factor]:
            errors.append(f"Invalid rating '{rating}' for effort multiplier {factor}")
    
    if errors:
        raise COCOMOIIError("\n".join(errors))

def get_scale_factor_value(factor, rating):
    """Get numeric value for a scale factor rating"""
    return SCALE_FACTORS[factor][rating]

def get_effort_multiplier_value(factor, rating):
    """Get numeric value for an effort multiplier rating"""
    return EFFORT_MULTIPLIERS[factor][rating]

def compute_e(sfs):
    """Calculate the scaling exponent E"""
    sf_values = [get_scale_factor_value(f, r) for f, r in sfs.items()]
    return B + 0.01 * sum(sf_values)

def calculate_effort(size_ksloc, ems, sfs):
    """
    Calculate effort in person-months
    Args:
        size_ksloc: Size in thousands of SLOC
        ems: Dict of effort multiplier ratings (e.g., {'RELY': 'N', 'DATA': 'L'})
        sfs: Dict of scale factor ratings (e.g., {'PREC': 'N', 'FLEX': 'H'})
    Returns:
        tuple: (PM, E) where PM is effort in person-months, E is scaling exponent
    """
    validate_ratings(ems, sfs)
    
    E = compute_e(sfs)
    em_values = [get_effort_multiplier_value(f, r) for f, r in ems.items()]
    EM_product = math.prod(em_values)
    
    PM = A * (size_ksloc ** E) * EM_product
    return round(PM, 2), E