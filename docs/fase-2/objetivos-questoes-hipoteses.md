# Objetivos, Questões e Hipóteses (GQM)

## 1. Nível Conceitual — Objetivos de Medição (`G1` a `G4`)

Cada objetivo foi estruturado segundo o template formal de cinco elementos de Basili, Caldiera e Rombach (1994): **Analisar** *(objeto)*, **com o propósito de** *(propósito)*, **com respeito a** *(foco de qualidade)*, **do ponto de vista de** *(partes interessadas)* e **no contexto de** *(ambiente e recorte)*.

**Tabela 1 — Objetivos de medição GQM (`G1` a `G4`) e rastreabilidade com a Fase 1**

| ID | Analisar (Objeto) | Com o propósito de | Com respeito à (Foco de Qualidade) | Do ponto de vista de | No contexto de |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`G1`** | A configuração de infraestrutura conteinerizada e os endpoints da API REST dos módulos de Matrícula e Notas do i-Educar 2.12 | Diagnosticar e avaliar | **Compatibilidade** (*Coexistência* e *Interoperabilidade* — ISO/IEC 25010:2023) | Equipes de TI municipais e integradores de sistemas | Implantação em ambiente Docker compartilhado e integração de dados escolares via HTTP/JSON |
| **`G2`** | O motor de cálculo de boletins (`Boletim.php`), os serviços de escrita composta e os esquemas PostgreSQL (`pmieducar`, `modules`, `cadastro`) | Verificar e garantir | **Confiabilidade** (*Ausência de Falhas*, *Tolerância a Falhas* e *Recuperabilidade* — ISO/IEC 25010:2023) | Gestores das Secretarias Municipais, professores e secretários escolares | Processamento de médias/menções, movimentações de matrícula e rotinas de backup/restauração |
| **`G3`** | O código-fonte híbrido (`app/` em Laravel e `ieducar/` legado), os modelos `Legacy*` e a suíte de testes automatizados | Mensurar e caracterizar | **Manutenibilidade** (*Analisabilidade*, *Modularidade*, *Modificabilidade* e *Testabilidade* — ISO/IEC 25010:2023) | Mantenedores (Portabilis) e desenvolvedores da comunidade de software livre | Evolução contínua e manutenção corretiva/evolutiva dos módulos de Matrícula e Avaliação |
| **`G4`** | As interfaces e fluxos operacionais de Matrícula (`T1`) e Diário de Classe (`T2`), bem como as mensagens de validação | Avaliar e validar | **Capacidade de Interação** (ISO/IEC 25010:2023) e **Eficácia/Eficiência em Uso** (ISO/IEC 25019:2023) | Secretários escolares e professores iniciantes na plataforma | Operação cotidiana de secretaria e lançamento de notas sob supervisão experimental (TCLE) |

*Fonte: Elaborado pelos autores.*

---

## 2. Nível Operacional — Questões e Hipóteses (`Q1.1` a `Q4.4`)

Para tornar o julgamento empírico falsificável na Fase 4, cada uma das **14 questões operacionais** é acompanhada de uma **hipótese explícita** com limiar numérico.

### 2.1 Objetivo G1 — Compatibilidade

**Tabela 2 — Questões e hipóteses de Compatibilidade (`G1`)**

| Questão | Pergunta Operacional | Hipótese Testável (`H`) | Métrica Associada |
| :---: | :--- | :--- | :---: |
| **`Q1.1`** | Em que medida o i-Educar permite parametrizar e isolar seus recursos compartilháveis (portas, bancos, prefixos de cache e containers) para coexistir com outra instância no mesmo host sem colisão? | **`H1.1`:** Pelo menos $85\%$ dos recursos compartilháveis identificados permitem isolamento via variáveis de ambiente sem conflito ($\text{TINCR} \ge 85\%$). | `M1` (`TINCR`) |
| **`Q1.2`** | Qual a proporção de endpoints da API REST de Matrícula e Diário que cumprem integralmente os contratos JSON Schema em requisições válidas e retornam erros estruturados (sem HTTP 500 ou HTML) em requisições inválidas? | **`H1.2`:** Pelo menos $85\%$ dos endpoints avaliados atendem simultaneamente aos três critérios de contrato ($\text{CEI} \ge 85\%$). | `M2` (`CEI`) |

---

### 2.2 Objetivo G2 — Confiabilidade

**Tabela 3 — Questões e hipóteses de Confiabilidade (`G2`)**

| Questão | Pergunta Operacional | Hipótese Testável (`H`) | Métrica Associada |
| :---: | :--- | :--- | :---: |
| **`Q2.1`** | O motor de cálculo de médias, recuperações e arredondamentos (`Avaliacao_Service_Boletim`) produz resultados $100\%$ idênticos ao oráculo normativo escolar em todos os cenários de avaliação? | **`H2.1`:** O cálculo de notas e menções apresenta determinismo absoluto frente ao manifesto de oráculo ($\text{DCNM} = 100\%$). | **`Gate M3`** (`DCNM`) |
| **`Q2.2`** | As operações compostas de escrita em matrícula e lançamento de notas preservam atomicidade transacional (*rollback* total sob falha intermediária) e qual a densidade de defeitos operacionais observada? | **`H2.2`:** Fluxos que atravessam o código legado apresentam falhas de atomicidade ($\text{ITAE} < 100\%$), e a métrica $\text{DDOM}$ (`M5`) permanecerá não mensurável sem logs de produção de 90 dias. | **`Gate M4`** (`ITAE`)<br>`M5` (`DDOM`) |
| **`Q2.3`** | As rotinas de backup e restauração isolada dos esquemas críticos (`pmieducar`, `modules`, `cadastro`) reconstroem $100\%$ das tabelas, tuplas e restrições de integridade referencial? | **`H2.3`:** Pelo menos $95\%$ das unidades de backup/restauração planejadas são concluídas e verificadas sem perda de integridade ($\text{CVPB} \ge 95\%$). | `M6` (`CVPB`) |

---

### 2.3 Objetivo G3 — Manutenibilidade

**Tabela 4 — Questões e hipóteses de Manutenibilidade (`G3`)**

| Questão | Pergunta Operacional | Hipótese Testável (`H`) | Métrica Associada |
| :---: | :--- | :--- | :---: |
| **`Q3.1`** | Qual o nível de complexidade ciclomática estrutural típica (percentil 90) e de pico (máximo) dos métodos que implementam a lógica de Matrícula e Avaliação? | **`H3.1`:** A presença de controladores e serviços legados faz com que $\text{CC}_{P90} > 10$ ou $\text{CC}_{\max} > 20$ nos arquivos em escopo. | `M7a` (`CC-P90`)<br>`M7b` (`CC-MAX`) |
| **`Q3.2`** | Qual o grau de equilíbrio entre abstratividade ($A$) e instabilidade ($I$) dos pacotes e namespaces que compõem os módulos avaliados? | **`H3.2`:** Os componentes avaliados mantêm distância média da sequência principal de Martin moderada ($\text{DSPM} \le 0{,}30$). | `M8` (`DSPM`) |
| **`Q3.3`** | Qual a densidade de adaptações defensivas (mapeamentos de colunas legadas, *casts* forçados e supressões) exigida nos modelos Eloquent `Legacy*` para contornar o esquema histórico? | **`H3.3`:** O índice de fricção de dados nos modelos `Legacy*` supera o limiar ideal ($\text{IFDL} > 0{,}15$), refletindo o custo da arquitetura híbrida. | `M9` (`IFDL`) |
| **`Q3.4`** | Qual o Índice de Manutenibilidade Normalizado ($\text{MI}$) médio dos métodos pertencentes aos módulos de Matrícula e Notas? | **`H3.4`:** O Índice de Manutenibilidade médio permanece na faixa aceitável ($\text{MI} \ge 65$), mas com degradação acentuada nas classes de `ieducar/modules/Avaliacao/`. | `M10` (`MI`) |
| **`Q3.5`** | Qual a proporção de casos de teste automatizados de Matrícula e Avaliação que estão efetivamente ativos e executam asserções reais (sem `markTestSkipped()`)? | **`H3.5`:** A existência de suítes legadas desativadas com `markTestSkipped()` reduz a taxa de testes ativos para menos de $80\%$ ($\text{TTAE} < 80\%$). | `M11` (`TTAE`) |

---

### 2.4 Objetivo G4 — Capacidade de Interação e Qualidade em Uso

**Tabela 5 — Questões e hipóteses de Capacidade de Interação e Qualidade em Uso (`G4`)**

| Questão | Pergunta Operacional | Hipótese Testável (`H`) | Métrica Associada |
| :---: | :--- | :--- | :---: |
| **`Q4.1`** | O sistema bloqueia $100\%$ das submissões de entradas inválidas (notas fora da faixa, etapas bloqueadas, menções inexistentes e conflitos de matrícula) sem persistir dados corrompidos nem lançar erro 500? | **`H4.1`:** O sistema bloqueia $100\%$ dos cenários inválidos do catálogo sem corrupção de banco ou exceção não tratada ($\text{IPPE} = 100\%$). | **`Gate M12`** (`IPPE`) |
| **`Q4.2`** | As mensagens de erro e validação exibidas ao usuário identificam claramente a causa do problema e orientam a ação corretiva necessária? | **`H4.2`:** Pelo menos $80\%$ das mensagens de validação auditadas apresentam causa e ação corretiva claras ($\text{ADMV} \ge 80\%$). | `M13` (`ADMV`) |
| **`Q4.3`** | Quanto tempo usuários iniciantes levam para concluir uma matrícula com enturmação (`T1`) e o lançamento de notas de uma turma (`T2`) em comparação à referência especialista ($T_{\text{ref}}$)? | **`H4.3`:** A razão de tempo médio dos iniciantes em relação à referência permanece igual ou inferior a $2{,}0$ em ambas as tarefas ($R_{\text{tempo},T1} \le 2{,}0$ e $R_{\text{tempo},T2} \le 2{,}0$). | `M14a` (`TMET-T1`)<br>`M14b` (`TMET-T2`) |
| **`Q4.4`** | Qual a proporção de usuários iniciantes que conseguem concluir as tarefas críticas `T1` e `T2` com sucesso já na primeira submissão correta? | **`H4.4`:** Pelo menos $70\%$ das execuções das tarefas `T1` e `T2` resultam em sucesso na primeira tentativa ($\text{TSPT} \ge 70\%$). | `M15` (`TSPT`) |

*Fonte: Elaborado pelos autores.*
