import js from '@eslint/js'
import globals from 'globals'
import * as tseslint from 'typescript-eslint'

export default tseslint.config([
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
  },
])