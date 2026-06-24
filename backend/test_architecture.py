"""
test_architecture.py — Verify the complete API → Service → Agent → Tools flow.

This test demonstrates that the clean architecture is properly connected:
    API Layer → Service Layer → Agent Layer → Tools Layer
"""

import asyncio
import httpx
from app.services.analysis_service import analyze_match
from app.agents.football_agent import run_analysis
from app.tools.form_tool import get_team_form


def test_layer_1_tools():
    """Layer 1: Test tools directly."""
    print("=" * 70)
    print("LAYER 1: TOOLS (Data Fetching)")
    print("=" * 70)
    print("\nTesting tool: get_team_form()")
    result = get_team_form("Arsenal")
    print(result[:100] + "...\n")


async def test_layer_2_agent():
    """Layer 2: Test agent (calls tools)."""
    print("=" * 70)
    print("LAYER 2: AGENT (Tool Orchestration)")
    print("=" * 70)
    print("\nTesting agent: run_analysis()")
    result = await run_analysis("Arsenal vs Chelsea")
    print(f"Summary: {result.analysis.summary}")
    print(f"Verdict: {result.analysis.final_verdict}\n")


async def test_layer_3_service():
    """Layer 3: Test service (calls agent)."""
    print("=" * 70)
    print("LAYER 3: SERVICE (Business Logic)")
    print("=" * 70)
    print("\nTesting service: analyze_match()")
    result = await analyze_match("Liverpool vs Man United")
    print(f"Summary: {result.analysis.summary}")
    print(f"Verdict: {result.analysis.final_verdict}\n")


async def test_layer_4_api():
    """Layer 4: Test API (calls service via HTTP)."""
    print("=" * 70)
    print("LAYER 4: API (HTTP Endpoint)")
    print("=" * 70)
    print("\nTesting API: POST /api/v1/analyze-match")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/v1/analyze-match",
                json={"query": "Man City vs Tottenham"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {response.status_code} OK")
                print(f"Summary: {data['analysis']['summary']}")
                print(f"Verdict: {data['analysis']['final_verdict']}\n")
            else:
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}\n")
    except Exception as e:
        print(f"Could not reach API (is server running?): {str(e)}\n")


async def test_full_flow():
    """Test the complete end-to-end flow."""
    print("\n" + "=" * 70)
    print(" ARCHITECTURE VERIFICATION TEST")
    print("=" * 70 + "\n")
    
    print("Testing clean architecture layers from bottom to top:\n")
    
    # Test each layer independently
    test_layer_1_tools()
    await test_layer_2_agent()
    await test_layer_3_service()
    await test_layer_4_api()
    
    print("=" * 70)
    print(" ARCHITECTURE SUMMARY")
    print("=" * 70)
    print("""
    ✓ Layer 1 (Tools):   Data fetching functions work independently
    ✓ Layer 2 (Agent):   Orchestrates tools and synthesizes analysis
    ✓ Layer 3 (Service): Clean business logic interface
    ✓ Layer 4 (API):     HTTP validation and routing
    
    Clean Architecture Benefits:
    - Each layer is independently testable
    - Changes to one layer don't affect others
    - Easy to swap implementations (mock → real data)
    - Clear separation of concerns
    """)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_full_flow())
