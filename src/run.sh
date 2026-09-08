#!/usr/bin/env bash
# 🎓 EduCore — Sobe a plataforma do curso (Learn Run Fly)
# Uso: ./run.sh
set -euo pipefail

BOLD='\033[1m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}🎓 EduCore — Learn Run Fly${NC}"
echo ""

fail() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# ── 1. Node.js ────────────────────────────────────────────────
if ! command -v node >/dev/null 2>&1; then
  echo -e "${RED}❌ Node.js não encontrado.${NC}"
  echo ""
  echo "Instale o Node.js (versão 18 ou superior):"
  echo "  • Linux/macOS:  https://nodejs.org  (ou: nvm install --lts)"
  echo "  • Ubuntu/Deb:   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install -y nodejs"
  echo "  • macOS:        brew install node"
  exit 1
fi

NODE_MAJOR="$(node -e 'console.log(process.versions.node.split(".")[0])')"
if [ "$NODE_MAJOR" -lt 18 ]; then
  fail "Node.js $(node --version) encontrado, mas a plataforma exige v18+. Atualize em https://nodejs.org"
fi
echo -e "✅ Node.js $(node --version)"

# ── 2. npm ────────────────────────────────────────────────────
command -v npm >/dev/null 2>&1 || fail "npm não encontrado. Reinstale o Node.js (vem junto): https://nodejs.org"
echo -e "✅ npm $(npm --version)"

# ── 3. Validação do curso (opcional — usa uv ou python3) ──────
if [ -f "scripts/validate_structure.py" ]; then
  echo ""
  echo -e "${BOLD}📋 Validando estrutura do curso...${NC}"
  if command -v uv >/dev/null 2>&1; then
    uv run scripts/validate_structure.py || echo -e "${YELLOW}⚠️  Curso com pendências — a plataforma abre mesmo assim.${NC}"
  elif command -v python3 >/dev/null 2>&1; then
    python3 scripts/validate_structure.py || echo -e "${YELLOW}⚠️  Curso com pendências — a plataforma abre mesmo assim.${NC}"
  else
    echo -e "${YELLOW}⚠️  Nem uv nem python3 encontrados — pulando validação (opcional).${NC}"
    echo "   Dica: instale o uv (https://docs.astral.sh/uv/) para validar o contrato do curso."
  fi
fi

# ── 4. Dependências da plataforma ─────────────────────────────
cd platform
if [ ! -d node_modules ]; then
  echo ""
  echo -e "${BOLD}📦 Primeira execução — instalando dependências...${NC}"
  npm install --no-fund --no-audit || fail "npm install falhou. Verifique sua conexão e rode novamente."
fi

# ── 5. Sobe a plataforma ──────────────────────────────────────
echo ""
echo -e "${GREEN}🚀 Subindo a plataforma...${NC}"
echo -e "   O navegador abrirá em instantes. Para parar: ${BOLD}Ctrl+C${NC}"
echo ""
npm run dev
