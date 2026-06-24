"""
models/analysis.py — Pydantic models for the /analyze-match endpoint.

Defines the public API contract. Both request and response shapes are
versioned here so breaking changes are easy to detect.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AnalysisRequest(BaseModel):
    """Request model for POST /api/v1/analyze-match"""
    query: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Natural language match query, e.g. 'Analyze Arsenal vs Chelsea'",
        examples=["Analyze Arsenal vs Chelsea", "Who will win Man United vs Liverpool?"]
    )


class AnalysisDetail(BaseModel):
    """
    Structured analysis result returned by the agent.
    
    Each field corresponds to one dimension of the analysis.
    The agent synthesises these from multiple tool calls.
    """
    summary: str = Field(description="High-level overview of the match context")
    form: str = Field(description="Recent form for both teams")
    head_to_head: str = Field(description="Historical head-to-head record")
    league_position: str = Field(description="Current league standings for both teams")
    insights: str = Field(description="Key tactical or statistical insights")
    final_verdict: str = Field(description="Agent's prediction or conclusion")


class AnalysisResponse(BaseModel):
    """Response model for POST /api/v1/analyze-match"""
    analysis: AnalysisDetail
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis": {
                    "summary": "Arsenal (2nd) hosts Chelsea (6th) in a crucial London derby.",
                    "form": "Arsenal: WWWDW | Chelsea: LWDWL",
                    "head_to_head": "Last 5: Arsenal 2-1, Chelsea 0-1, Arsenal 3-1, Draw 2-2, Chelsea 2-0",
                    "league_position": "Arsenal: 2nd, 68 pts | Chelsea: 6th, 51 pts",
                    "insights": "Arsenal's home record is strong (12W-2D-1L). Chelsea struggles away.",
                    "final_verdict": "Arsenal are favorites given form and home advantage."
                }
            }
        }
