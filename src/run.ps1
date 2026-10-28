# 🎓 Didatik — Sobe a plataforma do curso (Learn Run Fly)
# Uso: .\run.ps1

$ErrorActionPreference = "Stop"

Write-Host "🎓 Didatik — Learn Run Fly" -ForegroundColor Cyan
Write-Host ""

# Aviso MAX_PATH (260 chars) em Windows anterior ao 10
$osMajor = [System.Environment]::OSVersion.Version.Major
if ($osMajor -lt 10) {
  Write-Host "⚠️  Windows $osMajor detectado: limite de caminho de 260 caracteres." -ForegroundColor Yellow
  Write-Host "   Mantenha o projeto em pasta curta (ex: C:\cursos\meu-curso) para evitar erros." -ForegroundColor Yellow
  Write-Host ""
}

function Fail($msg) {
  Write-Host "❌ $msg" -ForegroundColor Red
  exit 1
}

# ── 1. Node.js ────────────────────────────────────────────────
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
  Write-Host "❌ Node.js não encontrado." -ForegroundColor Red
  Write-Host ""
  Write-Host "Instale o Node.js (versão 18 ou superior):"
  Write-Host "  • Download:     https://nodejs.org"
  Write-Host "  • Via winget:   winget install OpenJS.NodeJS.LTS"
  exit 1
}

$nodeMajor = [int](node -e "console.log(process.versions.node.split('.')[0])")
if ($nodeMajor -lt 18) {
  Fail "Node.js $(node --version) encontrado, mas a plataforma exige v18+. Atualize em https://nodejs.org"
}
Write-Host "✅ Node.js $(node --version)"

# ── 2. npm ────────────────────────────────────────────────────
$npm = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npm) { Fail "npm não encontrado. Reinstale o Node.js (vem junto): https://nodejs.org" }
Write-Host "✅ npm $(npm --version)"

# ── 3. Validação do curso (opcional — usa uv ou python) ───────
if (Test-Path "scripts/validate_structure.py") {
  Write-Host ""
  Write-Host "📋 Validando estrutura do curso..."
  $validated = $false
  $uv = Get-Command uv -ErrorAction SilentlyContinue
  $py = Get-Command python -ErrorAction SilentlyContinue
  if ($uv) {
    uv run scripts/validate_structure.py
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠️  Curso com pendências — a plataforma abre mesmo assim." -ForegroundColor Yellow }
    $validated = $true
  } elseif ($py) {
    python scripts/validate_structure.py
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠️  Curso com pendências — a plataforma abre mesmo assim." -ForegroundColor Yellow }
    $validated = $true
  }
  if (-not $validated) {
    Write-Host "⚠️  Nem uv nem python encontrados — pulando validação (opcional)." -ForegroundColor Yellow
    Write-Host "   Dica: instale o uv (https://docs.astral.sh/uv/) para validar o contrato do curso."
  }
}

# ── 4. Dependências da plataforma ─────────────────────────────
Set-Location platform
if (-not (Test-Path "node_modules")) {
  Write-Host ""
  Write-Host "📦 Primeira execução — instalando dependências..."
  npm install --no-fund --no-audit
  if ($LASTEXITCODE -ne 0) { Fail "npm install falhou. Verifique sua conexão e rode novamente." }
}

# ── 5. Sobe a plataforma ──────────────────────────────────────
Write-Host ""
Write-Host "🚀 Subindo a plataforma..." -ForegroundColor Green
Write-Host "   O navegador abrirá em instantes. Para parar: Ctrl+C"
Write-Host ""
npm run dev
