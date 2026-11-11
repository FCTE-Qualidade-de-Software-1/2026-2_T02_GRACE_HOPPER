# Qualidade em uso: sessões supervisionadas (M14a, M14b e M15)

Roteiro operacional, ficha de observação e cálculo das métricas de qualidade em uso da [Issue #46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46). As fórmulas e faixas são as do [Framework GQM](../gqm_evaluation_framework.md) (M14 e M15) e o protocolo ético é o [TCLE](../termo_consentimento_livre_esclarecido.md).

!!! info "Situação da coleta"
    Instrumentos prontos. As sessões dependem do ambiente Docker com dados fictícios da Issue #38 e ainda não foram realizadas; por isso M14a, M14b e M15 estão **não mensuráveis** até o preenchimento das fichas.

## 1. Preparação

1. Subir o ambiente Docker do i-Educar 2.12 (commit `7903a3e`) com a base fictícia da Issue #38 e restaurar o mesmo estado da base antes de cada sessão.
2. Definir e imprimir os dados das tarefas: para T1, um aluno já cadastrado e a turma de destino; para T2, a turma de 10 alunos, o componente curricular, a etapa e as 10 notas a lançar.
3. Preparar a gravação de tela (com áudio, se autorizada no TCLE) e um cronômetro.
4. Atribuir a cada participante um código sequencial (`P01`, `P02`...). O nome aparece apenas no TCLE assinado, que fica fora do repositório.

## 2. Tempo de referência

Um integrante treinado executa cada tarefa 3 vezes, com a base restaurada entre as execuções. $T_{\text{ref},T}$ é a média das 3 execuções. Os tempos são registrados em `m14_tempo_referencia.csv`.

## 3. Roteiro da sessão

**Tabela 1 — Roteiro de cada sessão supervisionada**

| Etapa | O que o avaliador faz |
| :--- | :--- |
| 1. Consentimento | Lê o TCLE com o participante, colhe a assinatura e marca `tcle_assinado = sim`. Sem TCLE assinado, a sessão não acontece. |
| 2. Instrução | Lê a instrução padronizada: "Você vai realizar duas tarefas no sistema usando os dados desta ficha. Não posso ajudar durante as tarefas. Avise quando terminar." |
| 3. Tarefa T1 | Entrega a ficha de T1. Inicia o cronômetro quando o participante começa a ler a tarefa e para na confirmação de gravação da enturmação. |
| 4. Tarefa T2 | Entrega a ficha de T2. Inicia o cronômetro na leitura e para na confirmação de gravação das 10 notas. |
| 5. Conferência | Consulta o banco para verificar se a matrícula, a enturmação e as notas gravadas correspondem à ficha. |
| 6. Registro | Preenche as fichas em `m14_tmet.csv` e `m15_tspt.csv`, sem dados pessoais. |

*Fonte: elaborado pelos autores a partir do protocolo do Framework GQM.*

**Critérios de registro:**

- **Concluiu a tarefa:** o dado esperado foi gravado ao final, mesmo após erros. Só quem concluiu entra no TMET.
- **Sucesso na 1ª submissão (M15):** a primeira submissão gravou o dado correto, sem erro de validação, recarga da página, perda do que foi digitado nem ajuda do avaliador.
- **Desistência:** se o participante desistir, a tarefa é registrada como não concluída e o motivo vai em `observacoes`.

## 4. Fichas de registro

As fichas ficam em `docs/evidencias/g4_interacao_uso/` e já estão no repositório apenas com o cabeçalho, para serem preenchidas durante as sessões.

**Tabela 2 — Estrutura das fichas de registro**

| Arquivo | Colunas | Uma linha por |
| :--- | :--- | :--- |
| [`m14_tempo_referencia.csv`](../evidencias/g4_interacao_uso/m14_tempo_referencia.csv) | `tarefa`, `execucao`, `executor`, `tempo_min` | execução de referência (3 por tarefa) |
| [`m14_tmet.csv`](../evidencias/g4_interacao_uso/m14_tmet.csv) | `participante`, `tcle_assinado`, `tarefa`, `concluiu`, `tempo_min`, `observacoes` | participante e tarefa |
| [`m15_tspt.csv`](../evidencias/g4_interacao_uso/m15_tspt.csv) | `participante`, `tarefa`, `sucesso_1a_submissao`, `motivo_falha`, `conferencia_banco` | participante e tarefa |

*Fonte: elaborado pelos autores.*

Os tempos são registrados em minutos com decimais (por exemplo, `3,5`), e os campos de sim ou não usam `sim` e `nao`. Em `executor`, usa-se o código do integrante, não o nome.

## 5. Cálculo

```bash
python3 scripts/uso/calcular_m14_m15.py
```

O script aplica as fórmulas do Framework GQM e só reporta valores quando o protocolo é atendido: pelo menos 5 participantes com código válido e TCLE registrado, e 3 execuções de referência por tarefa. Caso contrário, lista as pendências e mantém as métricas como não mensuráveis.

**Tabela 3 — Métricas, faixas e hipóteses de G4 em uso**

| Métrica | Fórmula | Excelente | Bom | Regular | Crítico | Hipótese |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **M14a** — $R_{\text{tempo},T1}$ | $\text{TMET}_{T1} / T_{\text{ref},T1}$ | $\le 1{,}5$ | $(1{,}5, 2{,}0]$ | $(2{,}0, 3{,}0]$ | $> 3{,}0$ | H4.3: $1{,}5 < R_{\text{tempo}} \le 2{,}5$ em T1 e em T2 |
| **M14b** — $R_{\text{tempo},T2}$ | $\text{TMET}_{T2} / T_{\text{ref},T2}$ | $\le 1{,}5$ | $(1{,}5, 2{,}0]$ | $(2{,}0, 3{,}0]$ | $> 3{,}0$ | H4.3 (mesma hipótese) |
| **M15** — TSPT | execuções corretas na 1ª submissão ÷ execuções totais | $\ge 90\%$ | $[70\%, 90\%)$ | $[50\%, 70\%)$ | $< 50\%$ | H4.4: $\text{TSPT} \in [70\%, 90\%)$ |

*Fonte: Framework GQM, Tabela 4 e Tabela H4.*

## 6. Resultados

Pendentes até a realização das sessões. Após a coleta, esta seção recebe a tabela de tempos por participante, os valores de $T_{\text{ref}}$, $\text{TMET}$, $R_{\text{tempo}}$ e TSPT, o nível de cada métrica e o resultado das hipóteses H4.3 e H4.4.
