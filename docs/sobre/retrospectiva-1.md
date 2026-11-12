# Retrospectiva — Entrega 1

Registro oficial da retrospectiva conduzida pela equipe **Grace Hopper** após o fechamento da **Entrega 1 (Ponto de Controle 1)**, seguindo o roteiro de dinâmicas da disciplina **Qualidade de Software 1 (FGA0315)**.

- **Equipe e Projeto:** Grace Hopper · Avaliação do i-Educar
- **Data da Sessão:** `28/10/2026`
- **Facilitador:** Ítalo Alves Sampaio de Oliveira · **Relatoria:** Todos os integrantes
- **Commit de Registro Original:** [`2bb1ee0`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/commit/2bb1ee056d2b05d333439e1fe134a747aa122082) (`docs/Retrospectiva/Grace Hopper - Retrospectiva.docx`)

**Tabela 1 — Participantes da retrospectiva da Entrega 1**

| Nome Completo | Matrícula UnB | Papel na Dinâmica |
| :--- | :---: | :--- |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | Facilitador e Relator |
| **Arthur Soares Parente** | `23/2036770` | Participante e Relator |
| **Fábio Santos Araujo** | `22/2022082` | Participante e Relator |
| **Gabriel Barbaceli** | `21/1045122` | Participante e Relator |
| **Gustavo Silva Rodrigues** | `23/2036887` | Participante e Relator |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | Participante e Relator |

*Fonte: Registro da retrospectiva da equipe em 28/10/2026.*

---

## 1. Tarefa 1 — O Projeto como Filme ou Carro

> **Pergunta da dinâmica:** *Se o seu projeto fosse um filme ou um carro, qual seria e por quê?*

- **Escolha da equipe:** **Carro Peugeot 207**
- **Justificativa (resposta curta):** *"Pois precisa de muita manutenção."* — A metáfora sintetizou tanto a complexidade da arquitetura híbrida do objeto avaliado (**i-Educar**, que exige constante manutenção entre legado e moderno) quanto a necessidade de revisões frequentes nos artefatos documentais da própria equipe para manter artigo e GitPage sincronizados.

---

## 2. Atividade 2 — Dinâmica dos Três Porquinhos

A equipe avaliou a condução da Entrega 1 classificando as práticas em três estruturas: **Casa de Palha** (o que pôs a entrega em risco e precisa ser corrigido), **Casa de Madeira** (o que funcionou parcialmente e precisa ser aperfeiçoado) e **Casa de Tijolos** (o que sustentou a equipe e deve ser preservado).

<div class="gh-colunas">
<div class="gh-coluna">
<p class="gh-secao"><span>Casa de Palha (Fragilidades)</span></p>
<div class="gh-painel">
<a class="gh-item" href="#3-priorizacao-e-analise"><small>Risco identificado na E1</small><span>Demora para iniciar as tarefas do primeiro ponto de controle, gerando concentração de trabalho em cima da hora antes do alinhamento final da entrega.</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Casa de Madeira (A Aperfeiçoar)</span></p>
<div class="gh-painel">
<a class="gh-item" href="#3-priorizacao-e-analise"><small>Ponto de evolução</small><span>Equilibrar a participação contínua de todos os integrantes ao longo das semanas, evitando picos de esforço concentrados.</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Casa de Tijolos (Forças)</span></p>
<div class="gh-painel">
<a class="gh-item" href="#3-priorizacao-e-analise"><small>Práticas a preservar</small><span>Boa comunicação interna, revisão cruzada constante dos pull requests e proatividade na resolução de pendências técnicas.</span></a>
</div>
</div>
</div>

---

## 3. Priorização e Análise

Após discutir os registros das três casas, os 6 integrantes votaram nos tópicos prioritários de intervenção para a **Entrega 2**, selecionando os dois assuntos mais votados (unanimidade de 6 votos cada):

**Tabela 2 — Votação e priorização dos tópicos de melhoria**

| Código | Tópico Discutido pela Equipe | Votos | Priorizado para a Entrega 2? |
| :---: | :--- | :---: | :---: |
| `C1` | Responsabilidade no cumprimento antecipado das entregas | — | Integrado a `C2` |
| **`C2`** | **Participação contínua e engajamento semanal** | **`6`** | **Sim (Prioridade 1)** |
| `C3` | Estudo teórico prévio do projeto e das normas da disciplina | — | Acompanhamento geral |
| **`C4`** | **Revisão sistemática dos critérios de avaliação (rubricas)** | **`6`** | **Sim (Prioridade 2)** |

*Fonte: Votação unânime da equipe em 28/10/2026.*

---

## 4. Plano de Ação: Quê, Quem e Quando

Para cada tópico priorizado, a equipe estabeleceu uma ação prática que altera o processo de trabalho na **Entrega 2** e é monitorada por meio dos indicadores de gestão (**PSM/CID**):

**Tabela 3 — Plano de ação para a Entrega 2 e vínculo com métricas do PSM/CID**

| Código e Tópico Priorizado | O que Faremos (Ação Prática) | Quem Acompanhará | Métrica / Evidência de Verificação |
| :---: | :--- | :---: | :--- |
| **`C2` — Participação Contínua** | Cada integrante assume formalmente sua trilha de especialidade (2 issues de 6h nos milestones `M5`/`M6`), registrando progresso semanal e não se abstendo das decisões técnicas e revisões. | **Fábio Santos Araujo** | Movimentação semanal de issues, commits e PRs no GitHub, monitorada via **`TCM`** e [Painel em Tempo Real](../painel_projeto.md). |
| **`C4` — Revisão dos Critérios de Avaliação** | Antes de cada ponto de controle e do fechamento da Release E2, cada integrante deve validar sua entrega frente ao roteiro de verificação e critérios da rubrica da disciplina. | **Todos os integrantes** *(auditoria cruzada)* | Checklist de validação preenchido ([`esqueleto_validacao.md`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/blob/main/docs/artigo/esqueleto_validacao.md)) e indicador **`TRCD = 100%`** no build estrito. |

*Fonte: Elaborado pelos autores (dinâmicas adaptadas de FunRetrospectives: Os Três Porquinhos e Quê-Quem-Quando).*
