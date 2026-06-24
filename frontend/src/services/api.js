/**
 * services/api.js — API client for backend communication.
 *
 * Handles all HTTP requests to the FastAPI backend.
 * In development: proxied through Vite (see vite.config.js)
 * In production: uses VITE_API_URL environment variable
 */

// Use environment variable for production, fallback to proxy for development
const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1";

/**
 * Analyze a football match based on natural language query.
 *
 * @param {string} query - Natural language query (e.g., "Analyze Arsenal vs Chelsea")
 * @returns {Promise<Object>} Analysis response with structured data
 * @throws {Error} If the request fails
 */
export async function analyzeMatch(query) {
  const response = await fetch(`${API_BASE_URL}/analyze-match`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
    );
  }

  return response.json();
}

/**
 * Check backend health status.
 *
 * @returns {Promise<Object>} Health status object
 */
export async function checkHealth() {
  const healthUrl = import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/health`
    : "/health";

  const response = await fetch(healthUrl);
  if (!response.ok) {
    throw new Error("Backend health check failed");
  }
  return response.json();
}
