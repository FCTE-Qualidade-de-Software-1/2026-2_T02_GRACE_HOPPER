# Visão Geral do Produto: i-Educar

**Issue:** #02 — Levantamento Arquitetural e Contextualização do i-Educar (Milestone M1, Fase 1 da ISO/IEC 25040:2024)

**Relação com a Issue:** esta página contextualiza o produto avaliado e seu papel social. A descrição técnica detalhada está em [Arquitetura e Contextualização Técnica](architecture.md).

---

## 1. O que é o i-Educar

O i-Educar é um sistema de gestão escolar de código aberto. O próprio repositório oficial o descreve como "software livre de gestão escolar" (campo `description` do `composer.json`) e, na descrição do repositório no GitHub, como "o maior software livre de educação do Brasil". Seu código-fonte é distribuído sob a licença GPL-2.0-or-later (campo `license` do `composer.json`).

Segundo o repositório e a publicação do Banco Interamericano de Desenvolvimento, o software é de acesso público e gratuito e é mantido pela Portabilis, com a comunidade de desenvolvedores. A publicação do BID o descreve como ferramenta de apoio às comunidades educativas na melhoria da gestão escolar.

Os modelos de domínio presentes no código mostram o alcance funcional do sistema, entre eles:

- **Vínculo escolar:** matrícula (`LegacyRegistration`), enturmação (`LegacyEnrollment`) e situações escolares (`RegistrationStatus`).
- **Acompanhamento pedagógico:** notas por componente curricular (`LegacyDisciplineScore`), regras de avaliação (`LegacyEvaluationRule`) e frequência de alunos (`LegacyStudentAbsence`).
- **Registros de histórico escolar:** histórico escolar (`LegacySchoolHistory`).
- **Integração com o Censo Escolar:** o módulo Educacenso é distribuído no pacote `i-educar-educacenso-package`, e o núcleo contém o controlador `EducacensoController`.

---

## 2. Finalidade Social

Em redes públicas municipais, a gestão escolar produz dados que sustentam decisões sobre o direito à educação. Os principais registros são:

- quem está matriculado, em qual turma e em qual situação;
- quais notas e menções cada aluno recebeu e como elas foram calculadas;
- quais dados foram enviados ao Censo Escolar, operado pelo INEP.

Um sistema que registra esses dados de forma confiável contribui para dois objetivos da Agenda 2030 tratados no projeto:

- **ODS 4 (Educação de Qualidade):** a meta 4.1 trata da conclusão de educação primária e secundária de qualidade, e a meta 4.a trata de ambientes de aprendizagem seguros e inclusivos. O i-Educar pode apoiar a gestão dessas informações, mas o projeto não mede resultados de aprendizagem nem de conclusão de curso.
- **ODS 16 (Paz, Justiça e Instituições Eficazes):** a meta 16.6 trata de instituições eficazes, responsáveis e transparentes. Um registro escolar rastreável e cálculos de nota determinísticos favorecem a transparência administrativa, mas essa relação é qualitativa e não é quantificada pela avaliação.

As partes interessadas, seus papéis e a justificativa dos ODS estão detalhadas no [Relatório de Planejamento do Ponto de Controle 1](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md), seção 2.1.3 e 2.1.6.

---

## 3. Relação com a Avaliação de Qualidade

A avaliação trata o i-Educar como **objeto de avaliação**, não como produto da equipe. Seu escopo, definido no [Framework GQM](../gqm_evaluation_framework.md), é:

| Dimensão | Recorte |
| :--- | :--- |
| Módulos avaliados | Matrícula de alunos e lançamento de notas e menções. |
| Características ISO/IEC 25010:2023 | Compatibilidade, Confiabilidade, Manutenibilidade e Capacidade de Interação (com Qualidade em Uso, ISO/IEC 25019:2023). |
| Versão avaliada | Branch `2.12` do repositório `portabilis/i-educar`. |
| Ambiente | Instalação local com Docker, usando dados fictícios. |

A avaliação é diagnóstica e independente. Ela não é certificação nem homologação oficial do software, e não avalia a exportação para o Educacenso, que está em pacote separado.

---

## 4. Limites deste Documento

- A classificação do i-Educar como Bem Público Digital é uma afirmação da equipe. As fontes consultadas confirmam a licença livre e a manutenção pela Portabilis, mas não encontraram o registro formal dessa classificação.
- A contribuição do sistema aos ODS é descrita como potencial. Os indicadores oficiais dessas metas dependem de dados nacionais que a avaliação não coleta.
- Os fatos técnicos deste documento foram verificados no commit `7903a3efc7689942ee700007f86ed581023aad27` do branch `2.12`, conforme registrado na página de arquitetura.

---

## 5. Fontes

- Repositório oficial: <https://github.com/portabilis/i-educar>.
- Publicação do BID sobre o i-Educar: <https://knowledge.iadb.org/pt-br/conhecimento-aberto/codigo-para-desenvolvimento/solucao-de-codigo-aberto/i-educar>.
- Pacote Educacenso oficial: <https://github.com/portabilis/i-educar-educacenso-package>.
- Metas ODS 4 e 16 da ONU: <https://sdgs.un.org/goals/goal4> e <https://sdgs.un.org/goals/goal16>.
