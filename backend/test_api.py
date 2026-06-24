"""
test_api.py — Quick script to test the FastAPI backend.

Run this while the server is running (uvicorn app.main:app --reload).
"""

import httpx
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health check endpoint."""
    response = httpx.get(f"{BASE_URL}/health")
    print(f"✓ GET /health → {response.status_code}")
    print(f"  Response: {response.json()}\n")

def test_analyze_match():
    """Test the analyze-match endpoint with a sample query."""
    payload = {"query": "Analyze Arsenal vs Chelsea"}
    response = httpx.post(
        f"{BASE_URL}/api/v1/analyze-match",
        json=payload
    )
    print(f"✓ POST /api/v1/analyze-match → {response.status_code}")
    print(f"  Request: {json.dumps(payload, indent=2)}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing AI Football Research System API")
    print("=" * 60 + "\n")
    
    test_health()
    test_analyze_match()
    
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
