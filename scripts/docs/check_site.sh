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
DISABLE_MKDOCS_2_WARNING=true "$MKDOCS" build --strict

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

echo "Verificando se restaram links com href=\"docs/\" ou href=\"file:///\" no HTML..."
if grep -rn 'href="docs/' site/; then
    echo "Erro: links relativos não reescritos com href=\"docs/\" encontrados no HTML gerado!" >&2
    exit 1
fi

if grep -rn 'href="file:///' site/; then
    echo "Erro: links locais inválidos (href=\"file:///\") encontrados no HTML gerado!" >&2
    exit 1
fi

echo "Verificando fórmulas arithmatex (display e inline) na página GQM..."
GQM_HTML="site/gqm_evaluation_framework/index.html"
if [ ! -f "$GQM_HTML" ]; then
    echo "Erro: página $GQM_HTML não encontrada!" >&2
    exit 1
fi

if ! grep -q '<div class="arithmatex">' "$GQM_HTML"; then
    echo "Erro: blocos de equação '<div class=\"arithmatex\">' não encontrados em $GQM_HTML" >&2
    exit 1
fi

if grep -n '\$<span class="arithmatex">' "$GQM_HTML"; then
    echo "Erro: fórmulas mal formatadas com cifrão literal (\$<span class=\"arithmatex\">) encontradas em $GQM_HTML!" >&2
    exit 1
fi

echo "Verificando renderização de diagramas Mermaid..."
if ! grep -q 'class="mermaid"' "$GQM_HTML"; then
    echo "Erro: diagrama Mermaid não renderizado em $GQM_HTML!" >&2
    exit 1
fi

GESTAO_HTML="site/gestao_projeto_releases_milestones_issues/index.html"
if ! grep -q 'class="mermaid"' "$GESTAO_HTML"; then
    echo "Erro: diagrama Mermaid não renderizado em $GESTAO_HTML!" >&2
    exit 1
fi

PAINEL_HTML="site/painel_projeto/index.html"
if [ ! -f "$PAINEL_HTML" ] || ! grep -q 'id="painel-projeto"' "$PAINEL_HTML" || ! grep -q 'painel.js' "$PAINEL_HTML"; then
    echo "Erro: painel em tempo real ausente ou sem script em $PAINEL_HTML!" >&2
    exit 1
fi

echo "Verificando a página de indicadores PSM/CID e CSVs exportados..."
PSM_HTML="site/indicadores_psm/index.html"
if [ ! -f "$PSM_HTML" ]; then
    echo "Erro: página $PSM_HTML não encontrada!" >&2
    exit 1
fi

for csv_file in "issues.csv" "prs.csv" "milestones.csv" "serie_semanal.csv" "contribuicao.csv" "medicoes.csv"; do
    if [ ! -f "site/indicadores_psm/$csv_file" ]; then
        echo "Erro: arquivo CSV de evidência 'site/indicadores_psm/$csv_file' não foi gerado!" >&2
        exit 1
    fi
done

echo "Verificando gráficos e tabelas no painel de indicadores PSM/CID..."
if ! grep -q "Matriz de contribuição individual" "$PSM_HTML"; then
    echo "Erro: tabela de contribuição individual não encontrada em $PSM_HTML!" >&2
    exit 1
fi

if ! grep -q "Tempo de ciclo" "$PSM_HTML"; then
    echo "Erro: seção de tempo de ciclo não encontrada em $PSM_HTML!" >&2
    exit 1
fi

if ! grep -q "Registro cronológico de medições" "$PSM_HTML"; then
    echo "Erro: histórico de medições não encontrado em $PSM_HTML!" >&2
    exit 1
fi

echo "Verificando barra de navegação no header (abas e dropdowns) em site/index.html..."
if ! grep -q 'class="md-tabs"' site/index.html; then
    echo "Erro: barra de abas no header (class=\"md-tabs\") não encontrada em site/index.html!" >&2
    exit 1
fi

if ! grep -q 'class="gh-tab-dropdown"' site/index.html; then
    echo "Erro: menus dropdown do header (class=\"gh-tab-dropdown\") não encontrados em site/index.html!" >&2
    exit 1
fi

echo "Verificando o índice lateral direito (TOC) nas páginas de conteúdo..."
if ! grep -q 'class="md-sidebar md-sidebar--secondary"' "$PSM_HTML"; then
    echo "Erro: índice lateral direito (md-sidebar--secondary) ausente em $PSM_HTML!" >&2
    exit 1
fi

echo "Todas as verificações passaram com sucesso!"
exit 0
