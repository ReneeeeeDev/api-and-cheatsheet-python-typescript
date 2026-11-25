import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Redirige /api al backend Node (así no hay problemas de CORS)
    proxy: { "/api": "http://localhost:3000" },
  },
});
