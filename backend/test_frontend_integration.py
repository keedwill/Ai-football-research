"""
test_frontend_integration.py — Test frontend-backend integration.

This script simulates frontend API calls to verify the full stack works:
1. Health check
2. Match analysis request
3. Response validation
4. CORS headers verification
"""

import httpx
import json


def test_health_endpoint():
    """Test /health endpoint (used by frontend for backend availability)"""
    print("\n=== TEST 1: Health Check ===")
    response = httpx.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✅ Health check passed")


def test_cors_headers():
    """Test CORS headers are present"""
    print("\n=== TEST 2: CORS Headers ===")
    response = httpx.options(
        "http://localhost:8000/api/v1/analyze-match",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        }
    )
    print(f"Status: {response.status_code}")
    print(f"CORS Headers: {dict(response.headers)}")
    
    # Check CORS headers
    assert "access-control-allow-origin" in response.headers
    print("✅ CORS headers present")


def test_analyze_match_endpoint():
    """Test /api/v1/analyze-match endpoint (main frontend -> backend call)"""
    print("\n=== TEST 3: Analyze Match Endpoint ===")
    
    # Simulate frontend request
    payload = {"query": "Analyze Arsenal vs Chelsea"}
    print(f"Request: POST /api/v1/analyze-match")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = httpx.post(
        "http://localhost:8000/api/v1/analyze-match",
        json=payload,
        headers={
            "Origin": "http://localhost:5173",
            "Content-Type": "application/json",
        }
    )
    
    print(f"\nStatus: {response.status_code}")
    
    # Verify response structure matches frontend expectations
    data = response.json()
    print(f"\nResponse Structure:")
    print(f"  - Has 'analysis' key: {'analysis' in data}")
    
    if "analysis" in data:
        analysis = data["analysis"]
        required_fields = [
            "summary", "form", "head_to_head", 
            "league_position", "insights", "final_verdict"
        ]
        
        print(f"\nAnalysis fields:")
        for field in required_fields:
            present = field in analysis
            print(f"  - {field}: {'✅' if present else '❌'}")
            assert present, f"Missing field: {field}"
        
        print(f"\n📊 Sample Response:")
        print(f"Summary: {analysis['summary'][:80]}...")
        print(f"Verdict: {analysis['final_verdict'][:80]}...")
    
    assert response.status_code == 200
    print("\n✅ Match analysis endpoint passed")


def test_frontend_error_handling():
    """Test error response format"""
    print("\n=== TEST 4: Error Handling ===")
    
    # Send invalid request (empty query)
    payload = {"query": ""}
    response = httpx.post(
        "http://localhost:8000/api/v1/analyze-match",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Error Response: {response.json()}")
    
    assert response.status_code == 422  # Validation error
    print("✅ Error handling works correctly")


def test_full_flow():
    """Test complete user flow: Arsenal vs Chelsea"""
    print("\n=== TEST 5: Complete User Flow ===")
    print("Simulating: User enters 'Man City vs Tottenham' → Submit")
    
    payload = {"query": "Man City vs Tottenham"}
    response = httpx.post(
        "http://localhost:8000/api/v1/analyze-match",
        json=payload,
        headers={"Origin": "http://localhost:5173"}
    )
    
    data = response.json()
    analysis = data["analysis"]
    
    print("\n📱 Frontend would display:")
    print("=" * 60)
    print(f"SUMMARY: {analysis['summary']}")
    print(f"\nFORM:\n{analysis['form'][:200]}...")
    print(f"\nVERDICT: {analysis['final_verdict']}")
    print("=" * 60)
    
    assert "Man City" in analysis["summary"] or "Manchester City" in analysis["summary"]
    assert "Tottenham" in analysis["summary"]
    print("\n✅ Full flow test passed")


if __name__ == "__main__":
    print("=" * 70)
    print("FRONTEND-BACKEND INTEGRATION TESTS")
    print("=" * 70)
    print("\nTesting connection between:")
    print("  Frontend: http://localhost:5173 (React + Vite)")
    print("  Backend:  http://localhost:8000 (FastAPI + LangChain)")
    print()
    
    try:
        test_health_endpoint()
        test_cors_headers()
        test_analyze_match_endpoint()
        test_frontend_error_handling()
        test_full_flow()
        
        print("\n" + "=" * 70)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        print("\n🎉 Frontend is properly connected to backend!")
        print("\n📝 Next steps:")
        print("   1. Open http://localhost:5173 in your browser")
        print("   2. Try example queries:")
        print("      - Analyze Arsenal vs Chelsea")
        print("      - Liverpool vs Man United")
        print("      - Man City vs Tottenham")
        print()
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure both servers are running:")
        print("  - Backend: uvicorn app.main:app --reload --port 8000")
        print("  - Frontend: npm run dev (in frontend/)")
        exit(1)
