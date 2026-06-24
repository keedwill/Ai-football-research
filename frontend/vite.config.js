import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api requests to the FastAPI backend during development.
// This avoids CORS issues when running React on :5173 and FastAPI on :8000.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
