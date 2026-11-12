# Requisitante e Partes Interessadas (Stakeholders)

Em conformidade com a **ISO/IEC 25040:2024**, o mapeamento de partes interessadas distingue o **requisitante metodológico** (contexto acadêmico da disciplina), o **requisitante institucional representativo** (domínio público educacional) e os **perfis de usuários, operadores e mantenedores** afetados pela qualidade dos módulos avaliados.

---

## 1. Identificação dos Papéis na Avaliação

- **Requisitante Metodológica:** Docente da disciplina *Qualidade de Software 1 (FGA0315 — UnB/FGA)*, responsável pelas diretrizes do processo de avaliação e critérios de rubrica.
- **Requisitante Institucional (Cenário de Domínio):** Secretarias Municipais de Educação que adotam ou avaliam adotar o **i-Educar** como sistema estruturante de gestão escolar.
- **Equipe Avaliadora Independente:** Equipe **Grace Hopper** (6 graduandos em Engenharia de Software da UnB/FGA), sem conflito de interesses com a mantenedora do produto.

---

## 2. Matriz de Partes Interessadas, Critérios de Sucesso e Influência

A Tabela 1 relaciona cada parte interessada às suas necessidades, aos critérios de sucesso adotados e a como cada perfil influenciou a seleção das características e métricas na Fase 2.

**Tabela 1 — Partes interessadas, necessidades, critérios de sucesso e rastreabilidade com o GQM**

| Parte Interessada (Papel SQuaRE) | Necessidades e Expectativas Principais | Critério de Sucesso na Avaliação | Influência Direta no Projeto da Avaliação |
| :--- | :--- | :--- | :--- |
| **Secretários Escolares**<br>*(Usuário Final Primário)* | Realizar matrículas, enturmações, transferências e remanejamentos (`pmieducar.matricula`) com rapidez e sem gravar registros inconsistentes. | Bloqueio de $100\%$ das entradas inválidas (`Gate M12 = 100%`), mensagens explicativas (`M13 >= 90%`) e conclusão ágil da tarefa `T1` (`M14a <= 2,0`, `M15 >= 70%`). | Ponto de vista do **Objetivo G4**; definiu a Tarefa `T1` do protocolo de Qualidade em Uso e motivou o Gate Binário `M12`. |
| **Professores da Rede Pública**<br>*(Usuário Final Primário)* | Lançar notas numéricas, menções conceituais e faltas no diário eletrônico sem perda de dados e com cálculo exato das médias. | Exatidão absoluta do boletim frente ao oráculo (`Gate M3 = 100%`), atomicidade no salvamento (`Gate M4 = 100%`) e fluidez na Tarefa `T2` (`M14b <= 2,0`). | Ponto de vista dos **Objetivos G2 e G4**; motivou o Gate Binário `M3` sobre `Avaliacao_Service_Boletim` e a Tarefa `T2`. |
| **Gestores das Secretarias Municipais**<br>*(Requisitante / Adquirente)* | Garantir a fidedignidade dos históricos escolares, a continuidade do serviço público e a prestação de contas da rede municipal. | Aprovação nos **3 Gates Binários**, restauração confiável de backups (`M6 >= 95%`) e índice global satisfatório ($\text{IQM} \ge 2{,}75$). | Motivou a atribuição do peso máximo (**30%**) para **Confiabilidade** e a regra não-compensatória dos Gates. |
| **Equipes de TI Municipais**<br>*(Operador / Integrador)* | Implantar o sistema em infraestrutura conteinerizada compartilhada e integrar dados com outros sistemas via API REST (`routes/api.php`). | Isolamento de portas/bancos/cache por variáveis de ambiente (`M1 >= 85%`) e aderência estrita aos contratos JSON Schema (`M2 >= 85%`). | Ponto de vista do **Objetivo G1**; motivou a inclusão da característica **Compatibilidade** (peso **20%**). |
| **Mantenedores (Portabilis e Comunidade)**<br>*(Desenvolvedor / Mantenedor)* | Evoluir a camada moderna (`app/`) e dar manutenção ao núcleo legado (`ieducar/`) com baixo risco de regressão e testes confiáveis. | Complexidade controlada (`M7a <= 10`, `M7b <= 20`), baixo acoplamento (`M8 <= 0,30`), baixo atrito nos modelos `Legacy*` (`M9 <= 0,25`), bom `MI` (`M10 >= 65`) e testes ativos (`M11 >= 80%`). | Ponto de vista do **Objetivo G3**; motivou o peso máximo (**30%**) para **Manutenibilidade**. |
| **Sistemas do INEP / Educacenso**<br>*(Usuário Secundário Indireto)* | Receber dados consistentes de matrícula e rendimento escolar exportados a partir da base de dados municipal. | Ausência de tuplas órfãs ou médias corrompidas nas tabelas `pmieducar.matricula` e `modules.nota_aluno` (`Gates M3 e M4`). | Tratado como requisito indireto de integridade de dados em **Confiabilidade (`G2`)** (o pacote externo `i-educar-educacenso-package` fica fora do escopo direto). |

*Fonte: Elaborado pelos autores em conformidade com a ISO/IEC 25040:2024.*
