# Manutenibilidade: complexidade ciclomática e índice de manutenibilidade (M7a, M7b e M10)

Resultado da execução do motor estático da equipe (`scripts/evaluate-quality.php`) sobre o commit congelado do i-Educar, conforme a [Issue #43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43). As definições, fórmulas e faixas são as do [Framework GQM](../gqm_evaluation_framework.md) (M7a, M7b e M10) e o roteiro é o da Tabela 3 do [Plano de medição e testes](../plano_medicao_testes.md).

## 1. Execução

**Tabela 1 — Dados da execução da coleta**

| Item | Valor |
| :--- | :--- |
| Produto | `portabilis/i-educar`, commit `7903a3efc7689942ee700007f86ed581023aad27` |
| Instrumento | `scripts/evaluate-quality.php` versão 2.0.0, PHP 8.3.6, análise léxica com `token_get_all` |
| Data da coleta | 11/11/2026 |
| Comando | `php scripts/evaluate-quality.php --path=/caminho/i-educar --evidence-dir=docs/evidencias/g3_manutenibilidade` |
| Universo | 213 callables concretos nos 4 arquivos do manifesto; nenhuma declaração sem corpo foi encontrada |
| Evidências | [`m7_complexidade.json`](../evidencias/g3_manutenibilidade/m7_complexidade.json) e [`m10_mi.json`](../evidencias/g3_manutenibilidade/m10_mi.json), com o inventário completo por callable |

*Fonte: elaborado pelos autores.*

## 2. Resultados

**Tabela 2 — Valores medidos, nível de pontuação e hipóteses de G3**

| Métrica | Valor medido | Nível ($S_i$) | Hipótese | Resultado da hipótese |
| :--- | :---: | :---: | :--- | :--- |
| **M7a** — $\text{CC}_{P90}$ | **8** (posto $r = \lceil 0{,}90 \times 213 \rceil = 192$) | Excelente (4) | H3.1: $10 < \text{CC}_{P90} \le 20$ e $\text{CC}_{\max} > 30$ | Refutada: o P90 ficou abaixo de 10 |
| **M7b** — $\text{CC}_{\max}$ | **72** (`Avaliacao_Service_Boletim::getSituacaoNotas`) | Crítico (1) | H3.1 (mesma hipótese) | O máximo acima de 30 se confirmou |
| **M10** — MI médio | **63,82** | Bom (3) | H3.4: $60 \le \text{MI} < 80$ | Confirmada |

*Fonte: elaborado pelos autores a partir da execução do motor estático no commit `7903a3e`.*

A distribuição explica a diferença entre M7a e M7b: 199 dos 213 callables (93,4%) têm $v(G) \le 10$, e a complexidade alta está concentrada em poucos métodos do núcleo legado. Como a H3.1 exige as duas condições, ela é refutada pelo P90, embora a parte do máximo tenha se confirmado.

**Tabela 3 — Distribuição de $v(G)$ nos 213 callables**

| Faixa de $v(G)$ | 1 a 5 | 6 a 10 | 11 a 15 | 16 a 20 | 21 a 50 | acima de 50 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Callables | 178 | 21 | 5 | 2 | 6 | 1 |

*Fonte: inventário por callable em `m7_complexidade.json`.*

**Tabela 4 — Distribuição do $\text{MI}_m$ nos 213 callables**

| Faixa de $\text{MI}_m$ | $\ge 80$ (Excelente) | $[60, 80)$ (Bom) | $[40, 60)$ (Regular) | $< 40$ (Crítico) |
| :--- | :---: | :---: | :---: | :---: |
| Callables | 20 | 123 | 61 | 9 |

*Fonte: inventário por callable em `m10_mi.json`.*

**Tabela 5 — Resultado por arquivo do manifesto**

| Arquivo | Callables | $v(G)$ médio | P90 do arquivo | $v(G)$ máximo | MI médio | LOC lógico |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `app/Services/RegistrationService.php` | 23 | 2,30 | 5 | 5 | 68,77 | 131 |
| `ieducar/modules/Avaliacao/Views/DiarioApiController.php` | 90 | 3,92 | 6 | 21 | 64,20 | 924 |
| `ieducar/modules/Avaliacao/Views/DiarioController.php` | 2 | 1,00 | 1 | 1 | 65,87 | 15 |
| `ieducar/modules/Avaliacao/Service/Boletim.php` | 98 | 5,21 | 11 | 72 | 62,27 | 1.317 |

*Fonte: elaborado pelos autores a partir do inventário por callable.*

O serviço migrado para Laravel (`RegistrationService`) tem os menores valores de complexidade e o maior MI médio. O `Boletim.php`, do núcleo legado, concentra o P90 mais alto e o máximo do universo.

**Tabela 6 — Os 10 callables de maior complexidade ciclomática**

| Arquivo | Callable | Linhas | $v(G)$ | LOC lógico | $\text{MI}_m$ |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `Boletim.php` | `getSituacaoNotas` | 937–1167 | 72 | 129 | 16,9 |
| `Boletim.php` | `getSituacaoFaltas` | 1215–1434 | 30 | 104 | 25,3 |
| `Boletim.php` | `promover` | 2731–2821 | 28 | 56 | 34,4 |
| `Boletim.php` | `_updateNotaComponenteMedia` | 2928–3113 | 26 | 82 | 28,6 |
| `DiarioApiController.php` | `Gerar` | 1982–2026 | 21 | 42 | 38,7 |
| `DiarioApiController.php` | `getEvaluationRule` | 1713–1826 | 21 | 71 | 31,5 |
| `DiarioApiController.php` | `getMatriculas` | 846–1028 | 21 | 59 | 32,5 |
| `Boletim.php` | `_calculateNotasRecuperacoesEspecificas` | 2464–2534 | 16 | 40 | 40,3 |
| `Boletim.php` | `verificaNotasLancadasNasEtapasAnteriores` | 3202–3303 | 16 | 40 | 39,8 |
| `Boletim.php` | `verificaSituacao` | 656–710 | 15 | 20 | 49,2 |

*Fonte: inventário por callable em `m7_complexidade.json`.*

## 3. Regras de medição aplicadas

- **Unidade:** callable concreto com corpo (método de classe, *trait* ou *enum*, ou função nomeada). Declarações abstratas e de interface seriam excluídas e listadas em `excluidos`; nesta execução não houve nenhuma. *Closures* e funções anônimas são contadas dentro do callable que as contém.
- **$v(G)$:** 1 + pontos de decisão no corpo: `if`, `elseif`, `for`, `foreach`, `while`, `case`, braço de `match` (exceto `default`), `catch`, `&&`, `||`, `and`, `or`, `??` e ternário. Para código estruturado, essa contagem equivale a $E - N + 2P$ do grafo de fluxo de controle.
- **Halstead:** operandos são variáveis, identificadores, nomes qualificados, literais e constantes mágicas; operadores são os demais tokens significativos. Parênteses, colchetes e chaves contam uma vez, na abertura. $HV = N \log_2 n$.
- **LOC lógico:** 1 (declaração) + instruções terminadas em `;` fora de parênteses + palavras-chave de estrutura de controle.
- **MI:** fórmula local normalizada do Framework GQM, limitada a $[0, 100]$; o MI de M10 é a média simples dos 213 valores.

## 4. Limitações

- A complexidade é obtida por contagem de pontos de decisão nos tokens, não pela construção explícita do grafo de fluxo; construções dinâmicas (por exemplo, chamadas por nome em texto) não são vistas pelo analisador.
- Os valores de Halstead e de LOC lógico dependem das regras de tokenização acima e não são comparáveis com ferramentas que usam outras convenções sem reprocessar os mesmos arquivos.
- O MI é um indicador aproximado de manutenibilidade e não prevê esforço ou defeitos.
- A reprodução exige o mesmo commit do produto e a mesma versão do instrumento; os testes do instrumento estão em `scripts/tests/evaluate_quality_test.php`.
