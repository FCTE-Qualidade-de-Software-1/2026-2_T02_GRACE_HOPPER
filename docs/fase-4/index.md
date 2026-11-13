# Fases 4 e 5: Executar e Concluir a Avaliação (Entrega 2)

As **Fases 4 e 5** correspondem às Atividades 4 (*Execute the evaluation*) e 5 (*Conclude the evaluation*) da **ISO/IEC 25040:2024** e compõem o escopo da **Entrega 2 (Ponto de Controle 2 — `v2.0.0-pc2`)**.

!!! info "Status Atual da Etapa"
    - **Situação:** Em execução (planejamento concluído e 12 issues atômicas `#38` a `#49` abertas e atribuídas nos milestones `M5` e `M6`).
    - **Acompanhamento ao vivo:** Consulte o progresso em tempo real no [Painel do Projeto](../painel_projeto.md) e no [Painel de Indicadores PSM/CID](../indicadores_psm.md).

---

## 1. Roteiro de Execução por Trilha (Fase 4 — Milestone `M5` e `M6`)

A execução empírica sobre o commit congelado `7903a3efc7689942ee700007f86ed581023aad27` do **i-Educar 2.12** está distribuída em seis trilhas técnicas:

**Tabela 1 — Cronograma operacional de coleta e julgamento para a Entrega 2**

| Trilha e Responsável | Issues | Métricas e Gates Executados | Entregável Técnico Esperado |
| :--- | :---: | :---: | :--- |
| **Trilha A — Infraestrutura e Backup**<br>*(Arthur Soares Parente)* | [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38), [#42](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/42) | `M1` (`TINCR`), `M6` (`CVPB`) | Ambiente Docker populado, tabela de isolamento de recursos e logs de `pg_dump`/`pg_restore` com validação SHA-256 nos esquemas `pmieducar`, `modules` e `cadastro`. |
| **Trilha B — API REST e Proteção**<br>*(Gabriel Barbaceli)* | [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39), [#45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45) | `M2` (`CEI`), **`Gate M12`** (`IPPE`), `M13` (`ADMV`) | Contratos JSON Schema validados, bateria de $\ge 12$ cenários de entradas inválidas e classificação independente por pares das mensagens de erro. |
| **Trilha C — Confiabilidade e Oráculo**<br>*(Gustavo Silva Rodrigues)* | [#40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40), [#41](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/41) | **`Gate M3`** (`DCNM`), **`Gate M4`** (`ITAE`), `M5` (`DDOM`) | Execução do manifesto de oráculo sobre `Boletim.php`, injeção de falhas em transações compostas com conferência SQL e registro formal de `M5`. |
| **Trilha D — Análise Estática e Testes**<br>*(Ítalo Alves Sampaio)* | [#43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43), [#44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44) | `M7a`, `M7b`, `M8`, `M9`, `M10`, `M11` | Relatório JSON/tabular extraído por `scripts/evaluate-quality.php` e resultado da execução da suíte Pest/PHPUnit dos módulos avaliados. |
| **Trilha E — Qualidade em Uso e Julgamento**<br>*(Ricardo Lucas Winchello)* | [#46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46), [#47](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/47) | `M14a`, `M14b` (`TMET`), `M15` (`TSPT`) + Cálculo de $\text{IQC}_k$ e $\text{IQM}$ | Coleta com $\ge 5$ participantes iniciantes (`P01`–`P05`) sob TCLE nas tarefas `T1`/`T2`, memória de cálculo dos índices e parecer conclusivo da Fase 5. |
| **Trilha F — Artigo v2 e Release E2**<br>*(Fábio Santos Araujo)* | [#48](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/48), [#49](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/49) | Consolidação Científica e Auditoria PSM/CID | Seções de Resultados, Discussão, Ameaças à Validade e Conclusão no artigo IEEE (`main.pdf`), slides finais do PC2 e publicação da tag `v2.0.0-pc2`. |

*Fonte: Elaborado pelos autores.*

---

### 1.1 Resultados e roteiros por métrica

- [Manutenibilidade (M7a, M7b e M10)](manutenibilidade-m7-m10.md): resultado da execução do motor estático sobre o commit congelado.
- [Qualidade em uso (M14a, M14b e M15)](qualidade-em-uso-m14-m15.md): métricas declaradas não mensuráveis antes da coleta e renormalização do $\text{IQC}_{\text{Interação}}$.

---

## 2. Estrutura do Julgamento na Fase 5

Ao concluir as coletas da Fase 4, esta seção será atualizada com:

1. **Veredito dos 3 Gates Binários Eliminatórios:** `Gate M3` (`DCNM`), `Gate M4` (`ITAE`) e `Gate M12` (`IPPE`).
2. **Tabela Consolidada das 17 Linhas Operacionais:** Valor bruto medido, enquadramento no nível $S_i \in \{1, 2, 3, 4\}$ e avaliação de cada hipótese (`H1.1` a `H4.4`: *Confirmada* ou *Refutada*).
3. **Cálculo dos Índices $\text{IQC}_k$ e $\text{IQM}$:** Enquadramento final na **Classe A**, **Classe B** ou **Classe C** e recomendações práticas por parte interessada.
