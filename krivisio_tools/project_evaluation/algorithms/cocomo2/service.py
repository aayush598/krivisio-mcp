#!/usr/bin/env python3
"""
service.py – COCOMO II Estimation Function (Modular)
"""

from krivisio_tools.project_evaluation.algorithms.cocomo2.constants import DEFAULT_EMS, DEFAULT_SFS
from krivisio_tools.project_evaluation.algorithms.cocomo2.sizing import FPCount, FPType, weight_fp_items, ufp_to_sloc, compute_size
from krivisio_tools.project_evaluation.algorithms.cocomo2.reuse import (
    ReuseParams, calc_esloc, su_from_rating, aa_from_rating, unfm_from_rating
)
from krivisio_tools.project_evaluation.algorithms.cocomo2.estimator import calculate_effort
from krivisio_tools.project_evaluation.algorithms.cocomo2.schedule import calculate_schedule

from krivisio_tools.project_evaluation.models.cocomo2_models import (
    SizingRequest, ReuseRequest, SLOCAdjustmentRequest, EffortScheduleRequest
)
from pydantic import BaseModel, Field
from typing import Dict


# Unified request model
class FullCOCOMOEstimationRequest(BaseModel):
    function_points: SizingRequest = Field(..., description="Function Point sizing input")
    reuse: ReuseRequest = Field(..., description="Reuse parameters")
    revl: SLOCAdjustmentRequest = Field(..., description="REVL adjustment")
    effort_schedule: EffortScheduleRequest = Field(..., description="Effort and schedule input")


def run_full_cocomo_estimation(
    request: FullCOCOMOEstimationRequest
) -> Dict[str, Dict[str, float]]:
    """
    Runs the complete COCOMO II estimation pipeline.

    Args:
        request (FullCOCOMOEstimationRequest): Combined input request

    Returns:
        dict: Output from sizing, reuse, revl, and estimation
    """

    # Step 1: Function Point to SLOC
    fp_counts = [
        FPCount(fp_type=FPType(it.fp_type), det=it.det, ftr_or_ret=it.ftr_or_ret)
        for it in request.function_points.fp_items
    ]
    ufp = weight_fp_items(fp_counts)
    sloc = ufp_to_sloc(ufp, request.function_points.language)

    # Step 2: Reuse → Equivalent SLOC
    reuse_params = ReuseParams(
        asloc=request.reuse.asloc,
        dm=request.reuse.dm,
        cm=request.reuse.cm,
        im=request.reuse.im,
        su=su_from_rating(request.reuse.su_rating),
        aa=aa_from_rating(request.reuse.aa_rating),
        unfm=unfm_from_rating(request.reuse.unfm_rating),
        at=request.reuse.at
    )
    esloc = calc_esloc(reuse_params)

    # Step 3: REVL adjustment
    size_result = compute_size(
        new_sloc=request.revl.new_sloc,
        adapted_esloc=request.revl.adapted_esloc,
        revl_percent=request.revl.revl_percent
    )

    # Step 4: Effort and schedule
    pm, E = calculate_effort(
        size_ksloc=request.effort_schedule.sloc_ksloc,
        ems=DEFAULT_EMS,
        sfs=DEFAULT_SFS
    )
    tdev = calculate_schedule(
        pm=pm,
        E=E,
        sced_rating=request.effort_schedule.sced_rating,
        pm_includes_sced=True
    )

    return {
        "function_point_sizing": {
            "ufp": ufp,
            "sloc": sloc
        },
        "reuse": {
            "esloc": round(esloc, 2)
        },
        "revl_adjustment": {
            "sloc_total": round(size_result.sloc, 2),
            "sloc_after_revl": round(size_result.sloc_after_revl, 2)
        },
        "estimation": {
            "person_months": round(pm, 2),
            "development_time_months": round(tdev, 2),
            "avg_team_size": round(pm / tdev, 2)
        }
    }
