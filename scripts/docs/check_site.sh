#!/usr/bin/env bash
set -euo pipefail

# Garante execução a partir da raiz do repositório
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Identifica o executável do mkdocs (.venv-docs ou PATH)
if [ -x ".venv-docs/bin/mkdocs" ]; then
    MKDOCS=".venv-docs/bin/mkdocs"
elif command -v mkdocs >/dev/null 2>&1; then
    MKDOCS="mkdocs"
else
    echo "Erro: mkdocs não encontrado em .venv-docs/bin/mkdocs nem no PATH" >&2
    exit 1
fi

echo "Executando mkdocs build --strict..."
"$MKDOCS" build --strict

echo "Validando site/index.html..."
if [ ! -f "site/index.html" ]; then
    echo "Erro: site/index.html não existe!" >&2
    exit 1
fi

README_TITLE="Avaliação de Qualidade de Software — i-Educar"
if ! grep -q "$README_TITLE" site/index.html; then
    echo "Erro: título do README ('$README_TITLE') não encontrado em site/index.html" >&2
    exit 1
fi

echo "Verificando se restaram links com href=\"docs/\" no HTML..."
if grep -rn 'href="docs/' site/; then
    echo "Erro: links relativos não reescritos com href=\"docs/\" encontrados no HTML gerado!" >&2
    exit 1
fi

echo "Verificando fórmulas arithmatex na página GQM..."
GQM_HTML="site/gqm_evaluation_framework/index.html"
if [ ! -f "$GQM_HTML" ]; then
    echo "Erro: página $GQM_HTML não encontrada!" >&2
    exit 1
fi

if ! grep -q 'class="arithmatex"' "$GQM_HTML"; then
    echo "Erro: class=\"arithmatex\" não encontrada em $GQM_HTML" >&2
    exit 1
fi

echo "Todas as verificações passaram com sucesso!"
exit 0
