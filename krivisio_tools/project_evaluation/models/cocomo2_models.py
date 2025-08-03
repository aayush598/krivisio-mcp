from typing import List, Literal
from pydantic import BaseModel, Field

# -----------------------------
# Function Point Item
# -----------------------------

class FPItemInput(BaseModel):
    fp_type: Literal["ILF", "EIF", "EI", "EO", "EQ"] = Field(..., description="Function Point type")
    det: int = Field(..., description="Data Element Types (DET)")
    ftr_or_ret: int = Field(..., description="FTRs or RETs depending on fp_type")

class SizingRequest(BaseModel):
    fp_items: List[FPItemInput] = Field(..., description="List of function point components")
    language: str = Field(..., description="Target programming language")

class FunctionPointToSLOCResponse(BaseModel):
    ufp: int = Field(..., description="Unadjusted Function Points")
    sloc: int = Field(..., description="Source Lines of Code")


# -----------------------------
# Reuse Estimation
# -----------------------------

class ReuseRequest(BaseModel):
    asloc: float = Field(..., description="Adapted Source Lines of Code")
    dm: float = Field(..., description="Design Modification (%)")
    cm: float = Field(..., description="Code Modification (%)")
    im: float = Field(..., description="Integration Modification (%)")
    su_rating: Literal["VL", "L", "N", "H", "VH"] = Field(..., description="Software Understanding Rating")
    aa_rating: Literal["0", "2", "4", "6", "8"] = Field(..., description="Assessment and Assimilation Rating")
    unfm_rating: Literal["CF", "MF", "SF", "CFa", "MU", "CU"] = Field(..., description="Unfamiliarity Rating")
    at: float = Field(0.0, description="Adaptation Time (%)")

class ReuseResponse(BaseModel):
    esloc: float = Field(..., description="Equivalent SLOC after adaptation")


# -----------------------------
# REVL Estimation
# -----------------------------

class SLOCAdjustmentRequest(BaseModel):
    new_sloc: float = Field(..., description="New source code SLOC")
    adapted_esloc: float = Field(0.0, description="Equivalent SLOC from reuse")
    revl_percent: float = Field(0.0, description="REVL (Requirements Evolution and Volatility) percentage")

class REVLResponse(BaseModel):
    sloc_total: float = Field(..., description="Total SLOC before REVL")
    sloc_after_revl: float = Field(..., description="Adjusted SLOC after REVL")


# -----------------------------
# Effort and Schedule Estimation
# -----------------------------

class EffortScheduleRequest(BaseModel):
    sloc_ksloc: float = Field(..., description="Total size in Kilo-SLOC (KSLOC)")
    sced_rating: Literal["VL", "L", "N", "H", "VH"] = Field("N", description="Schedule compression rating")

class EstimationResponse(BaseModel):
    person_months: float = Field(..., description="Estimated effort in Person-Months")
    development_time_months: float = Field(..., description="Estimated schedule in months")
    avg_team_size: float = Field(..., description="Average team size")


# -----------------------------
# Optional Unified Input Model
# -----------------------------

class ModelInput(BaseModel):
    model_name: str = Field(..., description="Estimation model to use (e.g., cocomo2)")
    data: dict = Field(..., description="Estimation input data")
