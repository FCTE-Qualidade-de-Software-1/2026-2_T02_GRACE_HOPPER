# Propósito da Avaliação e Uso Pretendido

## 1. Contexto e Problema Motivador

Redes públicas municipais de ensino dependem da exatidão dos registros de **matrícula, enturmação e transferência de alunos**, bem como da confiabilidade no **lançamento de notas, menções conceituais e cálculo de médias** ao longo do ano letivo.

A convivência arquitetural no **i-Educar 2.12** entre um núcleo legado em PHP procedural (`ieducar/intranet` e `ieducar/modules`) e uma camada moderna em Laravel (`app/`) sobre o mesmo banco PostgreSQL desperta quatro questões práticas:

1. **Coexistência e Integração:** A plataforma pode operar em infraestrutura municipal compartilhada sem colisão de recursos e manter contratos JSON estáveis em sua API REST?
2. **Exatidão Pedagógica e Integridade Transacional:** O motor de cálculo de boletins (`Avaliacao_Service_Boletim`) é 100% determinístico e as operações compostas de matrícula/diário garantem *rollback* integral em caso de falha?
3. **Sustentabilidade da Manutenção:** Qual o custo cognitivo e estrutural imposto pela ponte entre o código legado e os modelos modernos (`Legacy*`)?
4. **Proteção e Eficiência Operacional:** Secretários escolares e docentes conseguem realizar matrículas e lançamentos de notas sem induzir inconsistências na base e em tempo adequado?

---

## 2. Declaração Formal do Propósito

> **Propósito da Avaliação:** Diagnosticar de forma independente, objetiva e reprodutível o nível de qualidade dos módulos de **Matrícula de Alunos** e de **Lançamento de Notas e Menções** do **i-Educar 2.12** (commit `7903a3efc7689942ee700007f86ed581023aad27`), sob a ótica da **ISO/IEC 25010:2023** e **ISO/IEC 25019:2023**, fornecendo evidências quantitativas e qualitativas para apoiar decisões de **implantação municipal**, **priorização de refatorações**, **integração via API** e **capacitação de usuários**.

*Nota de escopo institucional:* Trata-se de uma avaliação acadêmica independente conduzida por avaliadores externos na disciplina FGA0315 (UnB/FGA), não constituindo certificação comercial ou homologação oficial junto ao MEC/INEP ou à Portabilis.

---

## 3. Uso Pretendido dos Resultados por Tomador de Decisão

A Tabela 1 sintetiza como os resultados e índices da avaliação ($\text{IQC}_k$, $\text{IQM}$ e Gates Binários) apoiam decisões práticas de cada grupo.

**Tabela 1 — Uso pretendido da avaliação e decisões apoiadas**

| Grupo Decisor | Decisão Apoiada pelos Resultados | Critério Objetivo de Apoio à Decisão |
| :--- | :--- | :--- |
| **Secretarias Municipais de Educação** *(Gestores / Adquirentes)* | Decidir pela adoção, atualização ou exigência de plano corretivo prévio antes de colocar a versão `2.12.0` em produção na rede escolar. | **Classe A** ($\text{IQM} \ge 3{,}25$ e 3 Gates aprovados): apto para produção.<br>**Classe B** ($2{,}75 \le \text{IQM} < 3{,}25$ e 3 Gates aprovados): adoção com plano de mitigação.<br>**Classe C** ($\text{IQM} < 2{,}75$ ou falha em Gate): bloqueio de release até correção. |
| **Mantenedores e Comunidade** *(Portabilis / Desenvolvedores)* | Priorizar o backlog técnico de refatoração, encapsulamento transacional e reativação de testes automatizados. | Métodos com $\text{CC}_{\max} > 20$ (`M7b`), modelos com alto atrito `IFDL` (`M9`) ou suítes com `markTestSkipped()` (`M11`) entram como prioridade alta de refatoração. |
| **Equipes de TI Municipais** *(Operadores / Integradores)* | Definir a topologia de implantação em containers e o uso direto dos endpoints REST para integração com portais municipais. | Se $\text{TINCR} \ge 85\%$ (`M1`), viabiliza coexistência parametrizada via `.env`; se $\text{CEI} \ge 85\%$ (`M2`), permite consumo direto sem camada adaptadora extra. |
| **Coordenações Pedagógicas e Escolas** *(Usuários Finais)* | Dimensionar a carga de treinamento e elaborar guias rápidos para secretários escolares e professores antes do início do bimestre. | Se $\text{ADMV} < 90\%$ (`M13`), $R_{\text{tempo}} > 2{,}0$ (`M14a/b`) ou $\text{TSPT} < 70\%$ (`M15`), recomenda-se oficina prática obrigatória e revisão das mensagens de erro. |

*Fonte: Elaborado pelos autores.*
