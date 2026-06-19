import nextPlugin from "eslint-config-next";

export default [
  ...nextPlugin,
  {
    ignores: ["**/*.test.ts", "**/*.test.tsx", "**/test/**"],
  },
];
