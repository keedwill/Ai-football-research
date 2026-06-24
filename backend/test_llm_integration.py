"""
test_llm_integration.py — Test OpenAI LLM integration.

Quick test to verify LLM is working before full system test.
"""

from app.config.settings import settings
from app.agents.football_agent import synthesize_analysis

def test_llm_synthesis():
    """Test LLM-powered analysis synthesis."""
    print("\n" + "=" * 70)
    print("LLM INTEGRATION TEST")
    print("=" * 70)
    
    # Check API key
    if not settings.openai_api_key:
        print("\n⚠️  OPENAI_API_KEY not set in .env file")
        print("   The system will use rule-based synthesis as fallback.")
        print("\n   To enable LLM:")
        print("   1. Add your OpenAI API key to backend/.env")
        print("   2. OPENAI_API_KEY=sk-proj-...")
        print("   3. Restart this test")
        print("\n   Continuing with fallback test...\n")
    else:
        print(f"\n✅ OPENAI_API_KEY detected: {settings.openai_api_key[:20]}...")
        print("   Testing LLM-powered synthesis...\n")
    
    # Sample data
    team_a = "Arsenal"
    team_b = "Chelsea"
    
    form_a = """Arsenal Recent Form: WWWDW
    Arsenal 3-1 Brentford (W)
    Wolves 1-2 Arsenal (W)
    Arsenal 2-2 Liverpool (D)
    West Ham 0-6 Arsenal (W)
    Arsenal 3-1 Crystal Palace (W)"""
    
    form_b = """Chelsea Recent Form: LDWLW
    Chelsea 2-1 Newcastle (W)
    Man United 2-1 Chelsea (L)
    Chelsea 1-1 Burnley (D)
    Aston Villa 1-0 Chelsea (L)
    Chelsea 3-2 Brighton (W)"""
    
    h2h = """Last 5 matches between Arsenal and Chelsea:
    Arsenal 5-0 Chelsea
    Chelsea 0-1 Arsenal
    Arsenal 3-1 Chelsea
    Chelsea 2-2 Arsenal
    Arsenal 1-2 Chelsea"""
    
    league_a = "Arsenal: Position 2/20 (68 points, 30 played, GD +43)"
    league_b = "Chelsea: Position 8/20 (45 points, 30 played, GD +8)"
    
    stats_a = "Arsenal: 71 scored, 28 conceded, xG 68.4, xGA 25.2"
    stats_b = "Chelsea: 52 scored, 44 conceded, xG 51.2, xGA 48.9"
    
    # Run synthesis
    print("🤖 Calling synthesis function...")
    try:
        result = synthesize_analysis(
            team_a, team_b,
            form_a, form_b, h2h,
            league_a, league_b,
            stats_a, stats_b
        )
        
        print("\n" + "=" * 70)
        print("ANALYSIS RESULT")
        print("=" * 70)
        
        print(f"\n📊 SUMMARY:")
        print(f"   {result.summary}")
        
        print(f"\n💡 INSIGHTS:")
        print(f"   {result.insights}")
        
        print(f"\n🎯 VERDICT:")
        print(f"   {result.final_verdict}")
        
        print("\n" + "=" * 70)
        
        # Detect if LLM was used
        if settings.openai_api_key and len(result.insights) > 100:
            print("✅ LLM SYNTHESIS SUCCESSFUL!")
            print("   The analysis shows sophisticated insights characteristic of GPT-4.")
        else:
            print("ℹ️  FALLBACK SYNTHESIS USED")
            print("   Using rule-based logic (no LLM).")
        
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPossible issues:")
        print("  - Invalid OPENAI_API_KEY")
        print("  - Network connectivity")
        print("  - API rate limits")
        print("\nThe system will fall back to rule-based synthesis.")
        return False


if __name__ == "__main__":
    success = test_llm_synthesis()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("\nNext steps:")
        print("  1. Add your OPENAI_API_KEY to backend/.env (if not already done)")
        print("  2. Restart the backend server")
        print("  3. Try a query via the frontend: http://localhost:5173")
        print("  4. Check logs for 'Using OpenAI LLM for analysis synthesis'")
    else:
        print("\n⚠️  Test completed with errors")
        print("   System will still work with fallback logic.")
