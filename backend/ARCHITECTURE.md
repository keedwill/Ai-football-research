# Backend Architecture Documentation

## Clean Architecture Implementation

The backend follows a strict **layered architecture** with clear separation of concerns:

```
┌────────────────────────────────────────────────────────────────┐
│  LAYER 4: API (HTTP)                                           │
│  File: app/api/routes.py                                       │
│  ├─ POST /api/v1/analyze-match                                 │
│  ├─ Validates request (Pydantic)                               │
│  ├─ Handles HTTP status codes                                  │
│  └─ Returns JSON response                                      │
└───────────────────────┬────────────────────────────────────────┘
                        │ calls analyze_match_service(query)
┌───────────────────────▼────────────────────────────────────────┐
│  LAYER 3: SERVICE (Business Logic)                             │
│  File: app/services/analysis_service.py                        │
│  ├─ async def analyze_match(query: str)                        │
│  ├─ Orchestrates workflow                                      │
│  ├─ Logging and monitoring                                     │
│  └─ Error handling                                             │
└───────────────────────┬────────────────────────────────────────┘
                        │ calls run_analysis(query)
┌───────────────────────▼────────────────────────────────────────┐
│  LAYER 2: AGENT (AI Orchestration)                             │
│  File: app/agents/football_agent.py                            │
│  ├─ async def run_analysis(query: str)                         │
│  ├─ Extracts team names from query                             │
│  ├─ Calls multiple tools in parallel                           │
│  ├─ Synthesizes results into analysis                          │
│  └─ Returns AnalysisResponse                                   │
└─────────┬──────────┬──────────┬──────────┬────────────────────┘
          │          │          │          │
          │ calls    │ calls    │ calls    │ calls
          ▼          ▼          ▼          ▼
┌─────────────┬─────────────┬─────────────┬─────────────────────┐
│  LAYER 1: TOOLS (Data Fetching)                               │
│  Directory: app/tools/                                         │
│  ├─ form_tool.py       → get_team_form(team_name)            │
│  ├─ h2h_tool.py        → get_head_to_head(team_a, team_b)    │
│  ├─ league_tool.py     → get_league_position(team_name)      │
│  └─ stats_tool.py      → get_team_statistics(team_name)      │
└────────────────────────────────────────────────────────────────┘
```

## Request Flow

### Example: "Analyze Arsenal vs Chelsea"

1. **API Layer** (`routes.py`)
   - Receives POST request
   - Validates with `AnalysisRequest` Pydantic model
   - Calls `analyze_match_service(query)`

2. **Service Layer** (`analysis_service.py`)
   - Logs request
   - Calls `run_analysis(query)`
   - Returns `AnalysisResponse`

3. **Agent Layer** (`football_agent.py`)
   - Extracts teams: "Arsenal" and "Chelsea"
   - Calls tools:
     - `get_team_form("Arsenal")`
     - `get_team_form("Chelsea")`
     - `get_head_to_head("Arsenal", "Chelsea")`
     - `get_league_position("Arsenal")`
     - `get_league_position("Chelsea")`
     - `get_team_statistics("Arsenal")`
     - `get_team_statistics("Chelsea")`
   - Synthesizes all data into structured analysis

4. **Tools Layer** (`tools/*.py`)
   - Each tool returns mock football data
   - Stateless, reusable functions
   - Easy to swap mock → real API calls

## Code Example

```python
# API Layer - routes.py
@router.post("/analyze-match")
async def analyze_match(request: AnalysisRequest):
    result = await analyze_match_service(request.query)
    return result

# Service Layer - analysis_service.py
async def analyze_match(query: str) -> AnalysisResponse:
    logger.info(f"Processing: {query}")
    result = await run_analysis(query)
    return result

# Agent Layer - football_agent.py
async def run_analysis(query: str) -> AnalysisResponse:
    team_a, team_b = extract_teams(query)

    # Call all tools
    form_a = get_team_form(team_a)
    form_b = get_team_form(team_b)
    h2h = get_head_to_head(team_a, team_b)
    # ... more tools

    # Synthesize analysis
    analysis = synthesize_analysis(...)
    return AnalysisResponse(analysis=analysis)

# Tools Layer - form_tool.py
def get_team_form(team_name: str) -> str:
    # Returns mock data
    return "Arsenal Recent Form: WWDWW..."
```

## Architecture Benefits

### ✓ Testability

Each layer can be tested independently:

- Tools → Unit tests
- Agent → Mock tools
- Service → Mock agent
- API → Mock service

### ✓ Maintainability

Changes to one layer don't affect others:

- Swap mock data → real API (tools only)
- Change analysis logic (agent only)
- Add authentication (API only)

### ✓ Scalability

Easy to extend:

- Add new tools → register in agent
- Add caching → service layer
- Add rate limiting → API layer

### ✓ Clear Contracts

Each layer has typed interfaces:

- `AnalysisRequest` → API input
- `AnalysisResponse` → API output
- Tools return `str` (simple, testable)

## Test Coverage

All layers verified:

- ✓ `test_tools.py` → Tests all 4 tools
- ✓ `test_agent.py` → Tests agent orchestration
- ✓ `test_api.py` → Tests HTTP endpoints
- ✓ `test_architecture.py` → Tests complete flow

## Future Enhancements

The architecture supports easy upgrades:

1. **Real APIs** → Update tools only
2. **LLM Integration** → Enhance agent synthesis
3. **Caching** → Add to service layer
4. **Rate Limiting** → Add to API layer
5. **Authentication** → Add to API middleware
