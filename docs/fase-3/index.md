# Fase 3: Projetar a Avaliação

A **Fase 3** corresponde à Atividade 3 da **ISO/IEC 25040:2024** (*Design the evaluation*). Nesta etapa, a equipe define o ambiente laboratorial reprodutível, os instrumentos de coleta estática e dinâmica, os manifestos congelados de casos de teste e o protocolo ético para as sessões com usuários.

!!! info "Distinção Metodológica Importante"
    Na Entrega 1 (`v1.0.0-pc1`), a Fase 3 especifica e valida os **instrumentos, roteiros e ambiente de medição**. A execução empírica sobre o checkout oficial congelado e a apuração dos valores finais de `M1` a `M15` constituem o escopo da **Fase 4 (Entrega 2)**.

---

## Subseções da Fase 3

<div class="gh-colunas">
<div class="gh-coluna">
<p class="gh-secao"><span>Infraestrutura e Instrumentos</span></p>
<div class="gh-painel">
<a class="gh-item" href="ambiente/"><small>Docker Compose · Commit 7903a3ef · PHP CLI</small><span>Ambiente Docker e ferramentas de coleta</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Roteiros Operacionais</span></p>
<div class="gh-painel">
<a class="gh-item" href="../plano_medicao_testes/"><small>Procedimentos detalhados de M1 a M15</small><span>Plano de medição e testes</span></a>
</div>
</div>

<div class="gh-coluna">
<p class="gh-secao"><span>Conformidade Ética e LGPD</span></p>
<div class="gh-painel">
<a class="gh-item" href="../termo_consentimento_livre_esclarecido/"><small>Participantes P01–P05 · Tarefas T1 e T2</small><span>Protocolo ético e TCLE</span></a>
</div>
</div>
</div>

---

## Síntese dos Instrumentos por Grupo de Métricas

**Tabela 1 — Instrumentos e métodos planejados para a coleta das 17 linhas operacionais**

| Objetivo GQM | Linhas Operacionais | Abordagem de Teste | Instrumentos e Ferramentas Planejados | Evidência a Produzir na Fase 4 |
| :---: | :---: | :--- | :--- | :--- |
| **`G1`**<br>*Compatibilidade* | `M1` (`TINCR`)<br>`M2` (`CEI`) | Caixa-cinza (Containers e Contratos de API) | `docker compose`, parametrização `.env` e validador de JSON Schema sobre `routes/api.php`. | Inventário de recursos compartilháveis, logs de subida simultânea e relatório HTTP/JSON por endpoint. |
| **`G2`**<br>*Confiabilidade* | `Gate M3` (`DCNM`)<br>`Gate M4` (`ITAE`)<br>`M5` (`DDOM`) · `M6` (`CVPB`) | Caixa-branca e Caixa-cinza (Oráculo e Banco) | Suíte Pest/PHPUnit (`NotaSituacaoCommon.php`), injeção de exceção em transações e `pg_dump`/`pg_restore` com SHA-256. | Tabela de casos do oráculo de notas, queries SQL antes/depois da falha injetada e log de restauração limpa. |
| **`G3`**<br>*Manutenibilidade* | `M7a`, `M7b`, `M8`, `M9`, `M10`, `M11` | Caixa-branca (Análise Estática e Runner de Testes) | Motor próprio `scripts/evaluate-quality.php` (PHP Tokenizer/AST) e runner Pest/PHPUnit. | JSON/CSV com $v(G_m)$, $HV_m$, $LOC_m$, $\text{MI}_m$ por método, matriz $A/I/D$ e contagem de `markTestSkipped()`. |
| **`G4`**<br>*Interação e Uso* | `Gate M12` (`IPPE`)<br>`M13`, `M14a`, `M14b`, `M15` | Caixa-preta e Sessões Supervisionadas | Catálogo de $\ge 12$ entradas inválidas, planilha de revisão dupla de mensagens e sessões cronometradas sob TCLE (`P01`–`P05`). | Status HTTP + conferência SQL pós-submissão, tabela de consenso de mensagens e planilha anonimizada de tempos $t_{k,T}$. |

*Fonte: Elaborado pelos autores.*

## Projeto e Cronograma Realizado da Avaliação

Na Entrega 2, cada linha operacional recebeu um universo congelado, um script de reprodução e uma issue com janela de execução registrada. A Tabela 2 reproduz a Tabela XII do artigo final.

**Tabela 2 — Universo congelado, tipo de teste, script de reprodução e janela realizada (abertura–fechamento da issue em 2026)**

| Métrica | Universo congelado | Tipo de teste | Reprodução (`scripts/`) | Issue e janela |
| :--- | :--- | :--- | :--- | :--- |
| `M1` | 16 recursos compartilháveis (portas, `container_name`, banco, Redis, volumes) | Caixa-cinza: duas instâncias simultâneas parametrizadas; baseline do compose oficial | `avaliacao/m1_coexistencia.sh` | `#38` · 08–12/11 |
| `M2` | 10 endpoints de leitura de Matrícula e Diário | Caixa-cinza: validação de contrato JSON | `avaliacao/m2_cei.py` | `#39` · 08–12/11 |
| `M3` | 30 casos do oráculo pedagógico | Caixa-branca: suíte determinística sobre `Boletim.php` | `avaliacao/m3/run.py` | `#40` · 08–13/11 |
| `M4` / `M5` | Operações multi-escrita de Matrícula e Diário; checklist D1–D5 | Caixa-cinza: injeção de falha e verificação no banco | `happy_path_op01.php` (pasta da rodada) | `#41` · 08–16/11 |
| `M6` | 6 cenários de backup e restauração | Caixa-cinza: `pg_dump`/`pg_restore` e contagem de tuplas e FKs | `avaliacao/m6/run_m6.sh` | `#42` · 08–16/11 |
| `M7` / `M10` | 213 callables em 4 arquivos | Caixa-branca: análise léxica (tokenização PHP) | `evaluate-quality.php` | `#43` · 08–13/11 |
| `M8`, `M9`, `M11` | Classes de domínio, models `Legacy*` e suíte Pest | Caixa-branca: análise estática e runner de testes | `evaluate-quality.php` e Pest | `#44` · 08–16/11 |
| `M12` / `M13` | 12 entradas inválidas | Caixa-preta: interface e API | `uso/avaliar_m12_m13.py` | `#45` · 08–16/11 |
| `M14` / `M15` | Tarefas T1 e T2 com ≥ 5 iniciantes | Sessões supervisionadas (não executadas: política prévia de 12/11) | Protocolo na GitPage | `#46` · 08–13/11 |
| Melhoria | `getSituacaoNotas` | Teste diferencial com semente fixa e nova medição estática | `melhoria/teste_equivalencia.php` | `#56` · 14–15/11 |

*Fonte: Elaborado pelos autores a partir do plano de medição, dos scripts e das issues do repositório.*

**Recursos.** Ambiente Docker local com PHP 8.5, Nginx 1.30, PostgreSQL 18 e Redis sobre o commit `7903a3e`, com a massa de dados fictícia do `DemoSeeder` (210 alunos e 210 matrículas). As versões ficam nos arquivos `environment.json` de cada evidência; CPU e memória não foram registradas, o que impede inferências de desempenho.

**Ajustes pré-coleta (08/11/2026).** O plano fixou, antes das coletas, a exclusão de `M5` do $\text{IQC}_{\text{Conf}}$ sem registros de produção, o intervalo Bom de `M6` em $[95\%, 100\%)$ e a ordem de classificação C → A → B.

**Cronograma.** O plano e as 12 issues de medição foram abertos em 08/11/2026 nos milestones `M5` e `M6`; a ação de melhoria (`#56`) foi aberta em 14/11, depois dos resultados de `M7`, e o artigo (`#48`) foi concluído em 21/11. Em 12/11, antes de qualquer coleta, `M14` e `M15` foram declaradas não mensuráveis ([detalhes](../fase-4/qualidade-em-uso-m14-m15.md)).
