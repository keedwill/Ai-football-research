# agents/__init__.py
# LangChain agent package.
# Each agent module here wires together:
#   - an LLM
#   - a set of tools (from tools/)
#   - a prompt / memory configuration
# Agents are the orchestration layer; they must NOT know about HTTP.
