import { defineConfig, searchForWorkspaceRoot } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    fs: {
      // Permite que o Vite leia os arquivos do curso (../curso) fora do root
      allow: [searchForWorkspaceRoot(process.cwd())],
    },
  },
})
