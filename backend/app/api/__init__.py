# api/__init__.py
# FastAPI router package.
# This layer owns HTTP concerns only:
#   - request validation (via Pydantic models)
#   - response serialisation
#   - HTTP status codes
# It delegates all business logic to the agents/ layer.
