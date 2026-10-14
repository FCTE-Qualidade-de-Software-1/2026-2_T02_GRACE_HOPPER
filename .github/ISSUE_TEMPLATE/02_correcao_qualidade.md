---
name: "Correção de Qualidade / Refatoração (GQM)"
about: "Template para resolução de débitos técnicos, falhas em gates e refatorações de código"
title: "[QUALIDADE] "
labels: ["qualidade", "refactor", "gqm-gate"]
assignees: []
---

## Identificação da Não-Conformidade ou Débito Técnico

- **Métrica / Gate Afetado**: [ ] Gate M3 (Determinismo de Notas) | [ ] Gate M4 (Integridade Transacional) | [ ] M7 (Complexidade) | [ ] M10 (Maintainability Index) | [ ] M11 (Testes Ativos) | [ ] Outro
- **Módulo / Componente**: [ ] Matrícula (`pmieducar.matricula` / `RegistrationService`) | [ ] Lançamento de Notas (`DiarioApiController` / `Boletim`) | [ ] APIs de Integração
- **Severidade da Não-Conformidade**: [ ] Blocker (Gate Binário Reprovado) | [ ] Alta | [ ] Média | [ ] Baixa

---

## Atribuição e Gestão de Esforço (PSM/CID — Critério AG-C5)

*Preencha os campos abaixo ao assumir esta issue:*

- **Responsável Principal**: [Preencher: Nome do Integrante]
- **Matrícula UnB**: [Preencher: 00/0000000]
- **Usuário GitHub**: @[Preencher: usuario]
- **Papel na Equipe**: [Preencher: ex. Engenheiro de Testes]
- **Valor da Hora de Trabalho (R$/h)**: R$ [Preencher: ex. 50,00]
- **Estimativa de Esforço**: [Preencher: ex. 3h]
- **Esforço Efetivo Realizado**: [Preencher ao concluir: ex. 3h]
- **Custo Efetivo da Issue**: R$ [Preencher ao concluir: horas * valor_hora]

---

## Descrição do Problema e Evidência

[Descreva a inconsistência observada, incluindo trechos de código, logs de teste ou a saída do motor de qualidade `php scripts/evaluate-quality.php`]

---

## Plano de Correção e Arquivos Afetados

- **Arquivos a Modificar**: `<caminho/do/arquivo>`
- **Estratégia de Correção**: [Descreva a solução técnica mínima e segura]

---

## Critérios de Aceitação e Verificação

- [ ] A alteração não introduz regressão funcional
- [ ] A métrica relacionada no `scripts/evaluate-quality.php` atinge o limiar esperado
- [ ] Testes unitários/integração executam com sucesso: `vendor/bin/pest <caminho_do_teste>`
- [ ] Registro de esforço preenchido nesta issue e no relatório de custos
