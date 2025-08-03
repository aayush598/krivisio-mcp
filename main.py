#!/usr/bin/env python3
"""
FastAPI Entry Point – Project Estimation API

Exposes an endpoint to run project estimation models via unified structure.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

from krivisio_tools.project_evaluation.main import run_estimation

app = FastAPI(
    title="Project Estimation API",
    version="1.0",
    description="Unified estimation endpoint supporting multiple algorithms like COCOMO II"
)


class EstimationInput(BaseModel):
    model_name: str = Field(..., description="Estimation model to run (e.g., cocomo2)")
    data: Dict[str, Any] = Field(..., description="Input data required by the model")


@app.post("/estimate")
def estimate(input_payload: EstimationInput):
    try:
        result = run_estimation(input_payload.model_name, input_payload.data)
        return {
            "model": input_payload.model_name.lower(),
            "result": result
        }
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Estimation error: {str(e)}")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Project Estimation API 🚀",
        "usage": "POST /estimate with model_name and data"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
