# Fase 1: Estabelecer os Requisitos da Avaliação

A **Fase 1** corresponde à Atividade 1 da **ISO/IEC 25040:2024** (*Establish the evaluation requirements*). Seu objetivo é definir com precisão **por que** o software está sendo avaliado, **para quem** os resultados se destinam, **qual** a arquitetura do produto, **quais** características da **ISO/IEC 25010:2023** são prioritárias e **qual** o recorte exato dos módulos inspecionados.

!!! info "Síntese da Fase 1 no Projeto Grace Hopper"
    - **Produto avaliado:** **i-Educar** (versão `2.12.0`, branch `2.12`, commit `7903a3efc7689942ee700007f86ed581023aad27`), sistema público de gestão escolar em PHP/Laravel e PostgreSQL.
    - **Módulos em escopo:** **1. Matrícula de Alunos** e **2. Lançamento de Notas e Menções (Diário/Boletim)**.
    - **Características selecionadas:** **Compatibilidade** (20%), **Confiabilidade** (30%), **Manutenibilidade** (30%) e **Capacidade de Interação / Qualidade em Uso** (20%).
    - **ODS vinculados:** **ODS 4** (Educação de Qualidade — Metas `4.1` e `4.a`) e **ODS 16** (Instituições Eficazes — Meta `16.6`).

---

## Subseções da Fase 1

<div class="gh-colunas">
<div class="gh-coluna">
<p class="gh-secao"><span>Contexto e Atores</span></p>
<div class="gh-painel">
<a class="gh-item" href="proposito/"><small>ISO/IEC 25040 · Atividade 1.1</small><span>Propósito da avaliação e uso pretendido</span></a>
<a class="gh-item" href="partes-interessadas/"><small>Requisitantes, usuários e mantenedores</small><span>Requisitante e partes interessadas</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Produto e Modelo</span></p>
<div class="gh-painel">
<a class="gh-item" href="produto/"><small>Monólito híbrido Laravel 13 + Legado PHP</small><span>Produto e componentes avaliados</span></a>
<a class="gh-item" href="modelo-qualidade/"><small>ISO/IEC 25010:2023 e ISO/IEC 25019:2023</small><span>Modelo de qualidade e priorização</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Recorte e Impacto Social</span></p>
<div class="gh-painel">
<a class="gh-item" href="escopo/"><small>Matrícula e Notas · Caixa-branca, cinza e preta</small><span>Escopo, profundidade e exclusões</span></a>
<a class="gh-item" href="ods/"><small>Agenda 2030 da ONU · ODS 4 e ODS 16</small><span>ODS, metas e indicadores relacionados</span></a>
</div>
</div>
</div>

---

## Documento Consolidado de Referência

Para consultar a redação contínua do planejamento da Entrega 1 em arquivo único, acesse o [Relatório de Planejamento — Ponto de Controle 1](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md).
