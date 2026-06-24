# services/__init__.py
# External data / integration layer.
# Services abstract away where data comes from (real API, mock, DB, cache).
# Agents and tools should call services — never call external APIs directly.
# This makes it easy to swap mock data for real providers without touching
# agent or tool logic.
