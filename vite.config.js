import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "static/dist",
    assetsDir: "",
    rollupOptions: {
      input: "src/js/main.js",
      output: {
        // This keeps filenames simple (main.js) instead of main.hash.js
        entryFileNames: `[name].js`,
        chunkFileNames: `[name].js`,
        assetFileNames: `[name].[ext]`,
      },
    },
  },
});
