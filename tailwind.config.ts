import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172238",
        brand: "#635BFF",
        mint: "#DDF7ED"
      }
    }
  },
  plugins: []
};

export default config;
