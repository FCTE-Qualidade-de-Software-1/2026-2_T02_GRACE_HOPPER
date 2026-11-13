# Qualidade em uso: M14a, M14b e M15 não mensuráveis

Registro da decisão da equipe sobre a [Issue #46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46). As definições das métricas estão no [Framework GQM](../gqm_evaluation_framework.md) (M14 e M15) e a política de cálculo está na seção 3.4 do [Plano de medição e testes](../plano_medicao_testes.md).

## 1. Decisão

**Tabela 1 — Situação das métricas de qualidade em uso na Entrega 2**

| Métrica | Situação | Hipótese | Situação da hipótese |
| :--- | :--- | :--- | :--- |
| **M14a** — $R_{\text{tempo},T1}$ (matrícula) | Não mensurável | H4.3: $1{,}5 < R_{\text{tempo}} \le 2{,}5$ em T1 e em T2 | Não testada |
| **M14b** — $R_{\text{tempo},T2}$ (diário) | Não mensurável | H4.3 (mesma hipótese) | Não testada |
| **M15** — TSPT | Não mensurável | H4.4: $\text{TSPT} \in [70\%, 90\%)$ | Não testada |

*Fonte: elaborado pelos autores.*

As três métricas dependem de sessões supervisionadas com no mínimo 5 participantes que nunca usaram o i-Educar, com TCLE assinado, cronometragem das tarefas T1 e T2, três execuções de referência por um integrante treinado e restauração do banco entre as sessões. Em 12/11/2026, **antes de qualquer coleta**, a equipe avaliou que essas sessões não cabem no cronograma da Entrega 2 e declarou as métricas não mensuráveis. Nenhum dado foi coletado, estimado ou substituído.

## 2. Impacto no julgamento

- M14a, M14b e M15 não recebem nota zero nem nota substituta.
- O $\text{IQC}_{\text{Interação}}$ é calculado apenas com M12 ($w = 2{,}0$) e M13 ($w = 0{,}8$), conforme a política pré-declarada da seção 3.4 do plano:

$$
\text{IQC}_{\text{Interação}} = \dfrac{S_{\text{M12}} \times 2{,}0 + S_{\text{M13}} \times 0{,}8}{2{,}8}
$$

- O peso de 20% de G4 no $\text{IQM}$ não muda. O resultado de G4 passa a representar apenas a capacidade de interação do produto (ISO/IEC 25010:2023).
- A qualidade em uso (ISO/IEC 25019:2023), ou seja, a eficiência e a eficácia de usuários iniciantes nas tarefas de matrícula e de lançamento de notas, fica **sem resultado nesta avaliação** e deve ser registrada como limitação no artigo.

## 3. Protocolo previsto para trabalho futuro

O protocolo abaixo não foi executado. Ele fica registrado para quem quiser medir M14 e M15 sobre o mesmo commit do produto.

**Tabela 2 — Roteiro previsto das sessões supervisionadas**

| Etapa | Procedimento |
| :--- | :--- |
| 1. Ambiente | Subir o i-Educar 2.12 (commit `7903a3e`) no Docker com dados fictícios e restaurar o mesmo estado do banco antes de cada sessão. |
| 2. Referência | Um integrante treinado executa T1 e T2 três vezes cada; $T_{\text{ref},T}$ é a média das três execuções. |
| 3. Consentimento | Cada participante assina o TCLE e recebe um código (`P01`, `P02`...); nenhum nome entra nos registros. |
| 4. Tarefas | T1: matricular e enturmar um aluno já cadastrado. T2: lançar as notas de um componente para uma turma de 10 alunos. O avaliador cronometra da leitura da tarefa até a confirmação de gravação e não ajuda o participante. |
| 5. Conferência | Consultar o banco após cada tarefa para verificar se os dados gravados correspondem à ficha. |
| 6. Cálculo | $\text{TMET}_T$ é a média dos tempos de quem concluiu a tarefa; $R_{\text{tempo},T} = \text{TMET}_T / T_{\text{ref},T}$; $\text{TSPT}$ é a razão entre execuções corretas na primeira submissão e execuções totais. |

*Fonte: elaborado pelos autores a partir do protocolo do Framework GQM.*
