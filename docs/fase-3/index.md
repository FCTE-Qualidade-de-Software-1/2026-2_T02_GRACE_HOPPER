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
