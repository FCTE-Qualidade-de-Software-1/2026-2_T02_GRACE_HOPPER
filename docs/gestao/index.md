# Gestão do Projeto (PSM/CID)

A equipe **Grace Hopper** acompanha o progresso, o esforço e a qualidade de processo do projeto utilizando o framework **PSM (*Practical Software and Systems Measurement*)**, adaptado para desenvolvimento contínuo e iterativo (**PSM/CID**).

Em conformidade com as diretrizes da disciplina **Qualidade de Software 1 (FGA0315)**, a gestão cobre as **três categorias fundamentais de informação** do PSM/CID, respondendo a questões gerenciais objetivas para apoiar decisões de replanejamento entre o **Ponto de Controle 1 (Entrega 1)** e o **Ponto de Controle 2 (Entrega 2)**.

**Tabela 1 — Categorias de informação do PSM/CID e indicadores adotados pela equipe**

| Categoria de Informação (PSM) | Indicador Adotado | Origem no PSM/CID | Pergunta Gerencial que Responde |
| :--- | :--- | :--- | :--- |
| **Calendário e Progresso** | **TCM** (*Taxa de Conclusão por Milestone*)<br>**ACM** (*Aderência ao Calendário dos Marcos*) | Parte 1, Tabela 5, linhas 1 e 3; Parte 2, seção 8.3 (*Committed vs. Completed*) | As tarefas planejadas para cada marco estão sendo concluídas dentro do cronograma previsto? |
| **Recursos e Custos** | **VEC** (*Variação de Esforço e Custo*) | Parte 1, Tabela 5, linhas 8 e 9 (*Estimate vs. Actual Effort*) | As estimativas de horas e orçamento ($R\$ 50,00/\text{h}$) refletem o esforço real dedicado pela equipe? |
| **Desempenho dos Processos** | **TRCD** (*Taxa de Revisão e Conformidade Documental*) | Parte 1, Tabela 5, linha 26 (*Process Compliance / Build & Peer Review*) | As entregas integradas à `main` passam pela validação automática estrita e por revisão de pares? |

*Fonte: Elaborado pelos autores com base em McGarry et al. (2002) e no guia PSM/CID (2021).*

---

## Ciclo do Processo de Medição

A organização desta seção reflete as três macroatividades do modelo de processo de medição do PSM: **Planejar a medição**, **Executar a medição** e **Avaliar os resultados para decidir ações de melhoria**.

```mermaid
flowchart LR
    subgraph P["1. Planejar"]
        P1["Planejamento de Marcos e Sprints<br/>(Milestones M0 a M6 e Trilhas)"]
        P2["Plano de Medição PSM<br/>(Fichas do Modelo de Informação)"]
    end
    subgraph M["2. Medir"]
        M1["Coleta Automática via GitHub API<br/>(scripts/psm/coletar_dados.py)"]
        M2["Painel PSM/CID e Horas/Custos<br/>(TCM, ACM, VEC, TRCD)"]
    end
    subgraph A["3. Avaliar e Decidir"]
        A1["Registro de Medições<br/>(Interpretação e Limitações)"]
        A2["Decisões e Melhoria Contínua<br/>(Replanejamento e Retrospectiva)"]
    end
    P --> M --> A
    A -.->|"Calibração para a Entrega 2"| P
```

**Figura 1 — Fluxo do processo de medição PSM/CID aplicado ao projeto. Fonte: adaptado de McGarry et al. (2002).**

---

## Navegação pelas Etapas de Gestão

<div class="gh-colunas">
<div class="gh-coluna">
<p class="gh-secao"><span>1. Planejar</span></p>
<div class="gh-painel">
<a class="gh-item" href="planejamento/"><small>Milestones M0 a M6 · Trilhas A–F · Releases</small><span>Planejamento de marcos e sprints</span></a>
<a class="gh-item" href="plano-de-medicao/"><small>Instâncias do modelo de informação (Aula 09)</small><span>Plano de medição do PSM</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>2. Medir</span></p>
<div class="gh-painel">
<a class="gh-item" href="../indicadores_psm/"><small>Gráficos SVG e CSVs gerados via GitHub Actions</small><span>Painel de indicadores PSM/CID</span></a>
<a class="gh-item" href="horas-custos/"><small>Critério AG-C5 · Memória de cálculo · 72h / R$ 3.600</small><span>Horas, custos e esforço</span></a>
<a class="gh-item" href="../painel_projeto/"><small>Consulta viva à API pública do GitHub</small><span>Painel em tempo real</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>3. Avaliar e Decidir</span></p>
<div class="gh-painel">
<a class="gh-item" href="registro-de-medicoes/"><small>Valores medidos, interpretação e ações E1 → E2</small><span>Registro de medições e decisões</span></a>
<a class="gh-item" href="../sobre/retrospectiva-1/"><small>Três Porquinhos e plano Quê-Quem-Quando</small><span>Retrospectiva da Entrega 1</span></a>
</div>
</div>
</div>

---

## Rastreabilidade Direta no GitHub

- **Milestones do repositório:** [Acessar Milestones M0 a M6](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/milestones)
- **Issues e Tarefas Atômicas:** [Acessar Issues no GitHub](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues)
- **Pull Requests e Revisões:** [Acessar Pull Requests](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pulls)
- **Catálogo completo de especificação de issues:** [Ver documento consolidado de Issues e Releases](../gestao_projeto_releases_milestones_issues.md)
