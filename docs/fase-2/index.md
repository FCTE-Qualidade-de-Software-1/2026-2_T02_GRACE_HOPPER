# Fase 2: Especificar a Avaliação (Framework GQM)

A **Fase 2** corresponde à Atividade 2 da **ISO/IEC 25040:2024** (*Specify the evaluation*). Utilizando a metodologia **GQM (*Goal-Question-Metric*)**, as quatro características priorizadas na Fase 1 são desdobradas em objetivos formais, questões operacionais acompanhadas de hipóteses testáveis, métricas com equações matemáticas rigorosas e critérios explícitos de julgamento.

!!! info "Contagem Oficial do Framework GQM (Versão 2.0)"
    - **4 Objetivos de Medição (`G1` a `G4`)** no template formal de 5 elementos de Basili, Caldiera e Rombach (1994).
    - **14 Questões Operacionais (`Q1.1` a `Q4.4`)** pareadas com **14 Hipóteses Verificáveis (`H1.1` a `H4.4`)**.
    - **15 Famílias de Métricas (`M1` a `M15`)** desdobradas em **17 Linhas Operacionais** (com `M7a`/`M7b` para complexidade ciclomática e `M14a`/`M14b` para tempo relativo nas tarefas `T1` e `T2`).
    - **3 Gates Binários Eliminatórios (`M3`, `M4` e `M12`)** não-compensatórios.

---

## Subseções da Fase 2

<div class="gh-colunas">
<div class="gh-coluna">
<p class="gh-secao"><span>Nível Conceitual e Operacional</span></p>
<div class="gh-painel">
<a class="gh-item" href="objetivos-questoes-hipoteses/"><small>G1 a G4 · Q1.1 a Q4.4 · H1.1 a H4.4</small><span>Objetivos, questões e hipóteses</span></a>
<a class="gh-item" href="rastreabilidade/"><small>Árvores GQM em Mermaid e Matriz F1 → F2</small><span>Diagrama GQM e rastreabilidade</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Nível Quantitativo</span></p>
<div class="gh-painel">
<a class="gh-item" href="metricas/"><small>M1 a M15 · 17 linhas operacionais · Fórmulas</small><span>Catálogo de métricas e Gates Binários</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Julgamento e Decisão</span></p>
<div class="gh-painel">
<a class="gh-item" href="niveis-julgamento/"><small>Escala 1–4 · Índices IQC e IQM · Classes A/B/C</small><span>Níveis de pontuação e julgamento</span></a>
<a class="gh-item" href="../gqm_evaluation_framework/"><small>Especificação contínua completa</small><span>Documento GQM consolidado</span></a>
</div>
</div>
</div>

---

## Quadro-Síntese da Estrutura GQM

**Tabela 1 — Visão geral dos 4 objetivos GQM, pesos, questões e métricas associadas**

| Objetivo GQM | Característica (ISO/IEC 25010 / 25019) | Peso no $\text{IQM}$ | Questões Operacionais | Famílias de Métricas (Linhas Operacionais) | Gates Binários |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **`G1`** | **Compatibilidade**<br>*(Coexistência e Interoperabilidade)* | **20%** | `Q1.1`, `Q1.2`<br>*(2 questões)* | `M1` (`TINCR`), `M2` (`CEI`)<br>*(2 linhas)* | — |
| **`G2`** | **Confiabilidade**<br>*(Ausência de Falhas, Tolerância e Recuperabilidade)* | **30%** | `Q2.1`, `Q2.2`, `Q2.3`<br>*(3 questões)* | `M3` (`DCNM`), `M4` (`ITAE`), `M5` (`DDOM`), `M6` (`CVPB`)<br>*(4 linhas)* | **`Gate M3`** (`100%`)<br>**`Gate M4`** (`100%`) |
| **`G3`** | **Manutenibilidade**<br>*(Analisabilidade, Modularidade, Modificabilidade e Testabilidade)* | **30%** | `Q3.1`, `Q3.2`, `Q3.3`, `Q3.4`, `Q3.5`<br>*(5 questões)* | `M7a` (`CC-P90`), `M7b` (`CC-MAX`), `M8` (`DSPM`), `M9` (`IFDL`), `M10` (`MI`), `M11` (`TTAE`)<br>*(6 linhas)* | — |
| **`G4`** | **Capacidade de Interação e Qualidade em Uso**<br>*(Proteção, Autodescritividade, Eficiência e Eficácia)* | **20%** | `Q4.1`, `Q4.2`, `Q4.3`, `Q4.4`<br>*(4 questões)* | `M12` (`IPPE`), `M13` (`ADMV`), `M14a` (`TMET-T1`), `M14b` (`TMET-T2`), `M15` (`TSPT`)<br>*(5 linhas)* | **`Gate M12`** (`100%`) |
| **TOTAL** | **4 Características Priorizadas** | **100%** | **14 Questões** | **15 Famílias (17 Linhas Operacionais)** | **3 Gates (`100%`)** |

*Fonte: Elaborado pelos autores.*
