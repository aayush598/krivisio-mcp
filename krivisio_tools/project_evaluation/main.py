"""
main.py – Project Estimation Engine

Provides a unified entry point for running project estimation algorithms like COCOMO II.
Designed to support multiple estimation models via dynamic dispatch.
"""

from typing import Dict, Any

from krivisio_tools.project_evaluation.algorithms.cocomo2.service import (
    run_full_cocomo_estimation,
    FullCOCOMOEstimationRequest
)

# Registry to map model names to their handlers and input models
ALGORITHM_REGISTRY = {
    "cocomo2": {
        "handler": run_full_cocomo_estimation,
        "request_model": FullCOCOMOEstimationRequest
    },
    # Add future algorithms like:
    # "putnam": {"handler": run_putnam_estimation, "request_model": PutnamEstimationRequest}
}


def run_estimation(model_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs the appropriate estimation algorithm based on the model name.

    Args:
        model_name (str): The algorithm to use (e.g., "cocomo2")
        data (dict): Input data in the expected format for the algorithm

    Returns:
        dict: Result of the estimation

    Raises:
        ValueError: If the model is unsupported or input is invalid
    """
    model_key = model_name.lower()

    if model_key not in ALGORITHM_REGISTRY:
        raise ValueError(f"Unsupported model: {model_name}")

    model_entry = ALGORITHM_REGISTRY[model_key]

    try:
        model_input = model_entry["request_model"](**data)
    except Exception as e:
        raise ValueError(f"Invalid input data: {str(e)}")

    return model_entry["handler"](model_input)


def get_available_models():
    """Returns the list of supported model names"""
    return list(ALGORITHM_REGISTRY.keys())
