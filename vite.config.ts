import { defineConfig } from "vite";
import { fresh } from "@fresh/plugin-vite";
import tailwindcss from "@tailwindcss/vite";
import daisyui from "daisyui";
export default defineConfig({
  plugins: [fresh(), tailwindcss(), daisyui()],
  root: "./src",
});
