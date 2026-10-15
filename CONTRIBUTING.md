# Guia de Contribuição e Governança da Equipe (FGA0315)

Este guia estabelece as diretrizes de governança, fluxo de trabalho Git, convenções de commits e procedimento de registro de esforço para os integrantes da equipe da disciplina **Qualidade de Software 1 (FGA0315 — UnB/FGA)**.

---

## 1. Fluxo de Trabalho e Atribuição de Issues

Para garantir a transparência da contribuição individual (**Critério AG-C5**) e a rastreabilidade do processo **PSM/CID**, o trabalho da equipe é organizado através de Issues no GitHub.

### 1.1 Como Assumir e Iniciar uma Tarefa
1. Consulte o catálogo de tarefas em [`docs/gestao_projeto_releases_milestones_issues.md`](docs/gestao_projeto_releases_milestones_issues.md) ou na aba **Issues** do repositório.
2. Ao selecionar uma issue para trabalhar:
   - Atribua a issue ao seu usuário do GitHub (*Assignee*).
   - Vincule a issue ao *Milestone* correspondente (ex.: `M1`, `M2`, `M3` ou `M4`).
   - Edite a issue e preencha seus dados de identificação e esforço:
     ```markdown
     - **Responsável Principal**: [Seu Nome Completo]
     - **Matrícula UnB**: [Sua Matrícula]
     - **Usuário GitHub**: @[seu_usuario]
     - **Papel na Equipe**: [Seu Papel — ex.: Especialista em Confiabilidade]
     - **Valor da Hora de Trabalho (R$/h)**: R$ [ex.: 50,00]
     - **Estimativa de Esforço**: [ex.: 4h]
     ```

### 1.2 Como Concluir e Registrar o Esforço Efetivo
Ao finalizar a tarefa e abrir o Pull Request correspondente:
1. Registre as **Horas Efetivas Realizadas** na issue e no documento de gestão:
   ```markdown
   - **Esforço Efetivo Realizado**: 4h
   - **Custo Efetivo da Issue**: R$ 200,00 (4h * R$ 50,00/h)
   ```
2. Atualize a sua linha correspondente na **Tabela 1** de [`docs/gestao_projeto_releases_milestones_issues.md`](docs/gestao_projeto_releases_milestones_issues.md) e na tabela do `README.md`.

---

## 2. Política de Branches (Padrão GitFlow Adaptado)

O repositório adota a seguinte convenção de branches para evitar conflitos e manter a integridade dos artefatos:

- **`main` / `master`**: Branch protegida contendo o código estável e as releases oficiais (`v1.0.0-pc1`, `v2.0.0-pc2`).
- **`develop`**: Branch de integração contínua onde as features aprovadas são unificadas antes dos pontos de controle.
- **`feature/issue-<num>-<descricao-curta>`**: Branches individuais de trabalho criadas a partir de `develop`.
  - Exemplo: `feature/issue-05-gqm-compatibilidade`
  - Exemplo: `feature/issue-11-motor-qualidade-php`
- **`docs/issue-<num>-<descricao-curta>`**: Branches dedicadas à documentação e redação do artigo científico.
  - Exemplo: `docs/issue-13-artigo-v1`

---

## 3. Padrão de Commits Semânticos (*Conventional Commits*)

Todas as mensagens de commit devem ser escritas em português ou inglês seguindo a especificação dos *Conventional Commits*:

```
<tipo>(<escopo>): <descrição no imperativo> #<numero_da_issue>
```

### Tipos Permitidos:
- **`docs`**: Alterações em documentação, relatórios, artigo acadêmico ou slides.
  - Exemplo: `docs(gqm): especificar metricas de compatibilidade M1 e M2 #05`
- **`feat`**: Adição de novo script de medição, funcionalidade ou template.
  - Exemplo: `feat(metrics): implementar calculo de complexidade P90 #11`
- **`fix`**: Correção de bug no código ou ajuste em fórmulas/tabelas inconsistentes.
  - Exemplo: `fix(framework): corrigir escala de pontuacao da metrica M10 #09`
- **`test`**: Criação ou reativação de testes unitários e de integração.
  - Exemplo: `test(avaliacao): reativar testes de nota em NotaSituacaoCommon #06`
- **`refactor`**: Refatoração de código sem alteração de comportamento externo.
  - Exemplo: `refactor(registration): adicionar transacao atomica em cancelamento #04`

---

## 4. Política de Pull Requests e Revisão por Pares (*Peer Review*)

1. **Vínculo Obrigatório à Issue**: O Pull Request deve conter na descrição a tag de fechamento automático (ex.: `Closes #05` ou `Fixes #06`).
2. **Revisão por Pares**: Todo PR exige a revisão e aprovação de pelo menos **um colega de equipe** antes do merge em `develop`.
3. **Critérios de Validação Pré-Merge**:
   - Os testes existentes continuam passando: `vendor/bin/pest` ou scripts locais.
   - O motor de avaliação de qualidade executa sem erro: `php scripts/evaluate-quality.php`.
   - A documentação e links compilam sem erro em modo estrito: `bash scripts/docs/check_site.sh` ou `mkdocs build --strict`.
   - Nenhum emoji foi introduzido em arquivos formais da disciplina (Critério AG-C3).
   - As tabelas e figuras adicionadas possuem numeração, legenda e fonte citada (Critérios AG-C2 e AG-C4).
