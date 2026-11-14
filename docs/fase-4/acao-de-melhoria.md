# Ação de melhoria: refatoração de `getSituacaoNotas`

Ação de melhoria da Entrega 2 ([Issue #56](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/56)), escolhida a partir dos resultados de manutenibilidade da [Fase 4](manutenibilidade-m7-m10.md). A melhoria é uma refatoração do método `Avaliacao_Service_Boletim::getSituacaoNotas` do i-Educar, entregue como *patch* sobre o commit avaliado, com teste de equivalência de comportamento e nova medição pelo motor estático da equipe.

## 1. Justificativa

**Tabela 1 — Resultados da Fase 4 que motivaram a ação**

| Evidência | Valor medido | Leitura |
| :--- | :--- | :--- |
| M7b — $\text{CC}_{\max}$ | **72** em `getSituacaoNotas` (Crítico, $S = 1$) | Único callable do universo com $v(G) > 30$. O segundo maior valor é 30 (`getSituacaoFaltas`). |
| $\text{MI}_m$ do método | **16,9** (faixa Crítica) | Método de 231 linhas físicas e 129 linhas lógicas, com o menor índice de manutenibilidade entre os 10 callables mais complexos. |
| Papel no produto | Cálculo da situação da matrícula (aprovado, reprovado, em exame, em andamento) | É a regra que define o resultado escolar do aluno, no mesmo domínio do Gate M3 (corretude do cálculo de notas e menções). |

*Fonte: elaborado pelos autores a partir de `m7_complexidade.json` e `m10_mi.json` (commit `7903a3e`).*

O método concentra, em um único bloco, cinco decisões diferentes: a regra de nota geral por etapa, a verificação de lançamentos incompletos, a progressão continuada, a situação de cada componente e os ajustes finais da situação geral. Por isso, alterar ou testar qualquer uma dessas regras exige entender o método inteiro. A ação ataca o pior valor medido em G3 sem mudar o que o sistema calcula.

## 2. O que foi alterado

A refatoração aplica *Extract Method*: cada decisão passou a ser um método privado com nome próprio, e `getSituacaoNotas` ficou responsável apenas por carregar os dados e coordenar as etapas. A assinatura pública, o valor de retorno e as exceções não mudaram.

**Tabela 2 — Métodos extraídos e complexidade de cada um**

| Método | Responsabilidade | $v(G)$ |
| :--- | :--- | :---: |
| `getSituacaoNotas` | Carrega médias e componentes e coordena o cálculo | 15 |
| `_idsDisciplinasNaoReprovativas` | Lista os componentes que não contam para a progressão | 1 |
| `_situacaoNotasPorMediaGeral` | Aplica a situação da média geral a todos os componentes | 3 |
| `_situacaoPorMediaGeral` | Converte média geral e etapa em situação | 12 |
| `_lancamentoNotasIncompleto` | Decide se ainda faltam médias lançadas | 7 |
| `_situacaoComponenteProgressaoContinuada` | Situação do componente na progressão continuada | 4 |
| `_situacaoComponentePorNota` | Situação do componente a partir da média e da regra | 17 |
| `_reprovadoPelaPrevisaoDeRecuperacao` | Reprovação automática pela nota prevista no exame | 4 |
| `_ajustarSituacaoGeralNotas` | Aprovação pela média das disciplinas e reprovação após dependências | 6 |

*Fonte: execução do motor estático sobre o arquivo com o patch aplicado.*

Também foi removido código sem efeito no resultado:

- a variável `$qtdComponenteReprovado`, que era incrementada em três pontos e nunca lida;
- as três chamadas a `exibeSituacao()` que só serviam para esse contador (o método apenas consulta as disciplinas aglutinadas e não altera estado);
- a inicialização `$media = 0`, sobrescrita antes de qualquer leitura.

**Escopo:** o patch [`getSituacaoNotas.patch`](../evidencias/melhoria/getSituacaoNotas.patch) se aplica ao commit `7903a3efc7689942ee700007f86ed581023aad27` e altera somente `ieducar/modules/Avaliacao/Service/Boletim.php`. O produto avaliado na Fase 5 continua sendo o commit congelado; os valores "depois" desta página mostram o efeito esperado caso a melhoria seja incorporada.

## 3. Verificação de que o comportamento não mudou

Uma refatoração só é melhoria se o resultado calculado continuar o mesmo. A equipe usou teste diferencial: o script [`scripts/melhoria/teste_equivalencia.php`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/blob/main/scripts/melhoria/teste_equivalencia.php) extrai `getSituacaoNotas` da versão original e da versão refatorada, executa as duas sobre os mesmos cenários e compara a saída.

- **Dublês:** as dependências de banco e de configuração (regra de avaliação, médias lançadas, componentes da matrícula, última etapa, previsão de recuperação, disciplina dispensada, disciplinas aglutinadas) são substituídas por objetos que devolvem os valores de cada cenário.
- **Cenários:** gerados de forma pseudoaleatória com semente fixa, combinando os tipos de nota, os tipos de progressão, as etapas numéricas e `Rc`, as regras de recuperação, de reprovação automática e de aprovação pela média, e as disciplinas dispensadas, aglutinadas e não reprovativas.
- **Comparação:** situação geral e situação de cada componente, na mesma ordem. Quando a versão original lança erro, a refatorada precisa lançar o mesmo erro com a mesma mensagem.
- **Autoteste:** o script injeta um defeito na versão refatorada e confirma que o teste o detecta, o que mostra que a comparação não passa por acaso.

**Tabela 3 — Resultado do teste de equivalência**

| Item | Valor |
| :--- | :--- |
| Cenários executados | 50.000 (semente 2026) |
| Situação geral na versão original | Aprovado 15.494 · Reprovado 4.034 · Em andamento 28.237 · Em exame 608 · Aprovado após exame 1.071 · Erro 556 |
| **Divergências entre original e refatorada** | **0** |
| Divergências com o defeito injetado | 779 (defeito detectado) |

*Fonte: [`equivalencia.txt`](../evidencias/melhoria/equivalencia.txt).*

Os 556 cenários com erro reproduzem um comportamento já existente no código original: quando uma disciplina aglutinada é removida por ser a disciplina dispensada da turma, a cópia da situação da primeira aglutinada acessa um componente inexistente. A refatoração preserva esse comportamento, porque mudá-lo alteraria o produto; ele fica registrado como achado para correção separada.

## 4. Resultado medido

**Tabela 4 — Métricas de G3 antes e depois da refatoração**

| Medida | Antes (commit `7903a3e`) | Depois (com o patch) |
| :--- | :---: | :---: |
| $v(G)$ de `getSituacaoNotas` | 72 | **15** |
| LOC lógico de `getSituacaoNotas` | 129 | 59 |
| $\text{MI}_m$ de `getSituacaoNotas` | 16,9 | 34,7 |
| Callables no universo | 213 | 221 |
| **M7a** — $\text{CC}_{P90}$ | 8 (Excelente) | 8 (Excelente) |
| **M7b** — $\text{CC}_{\max}$ | 72 (Crítico, $S = 1$) | **30** (Bom, $S = 3$), agora em `getSituacaoFaltas` |
| Callables com $v(G) > 30$ | 1 | 0 |
| **M10** — MI médio | 63,82 (Bom) | 63,79 (Bom) |

*Fonte: [`m7_complexidade.json`](../evidencias/melhoria/m7_complexidade.json) e [`m10_mi.json`](../evidencias/melhoria/m10_mi.json), gerados pelo `scripts/evaluate-quality.php` versão 2.0.0 sobre o arquivo com o patch.*

- **M7b** sai da faixa Crítica para a Boa. Como o peso de M7b no $\text{IQC}_{\text{Manutenibilidade}}$ é 1,2, a mudança de $S = 1$ para $S = 3$ acrescenta $2 \times 1{,}2 = 2{,}4$ pontos ponderados ao numerador do índice.
- **M10** praticamente não muda porque é a média simples dos callables: o método original sai da conta, mas entram oito métodos menores com $\text{MI}_m$ entre 45,9 e 74,1, abaixo da média do universo. O ganho de manutenibilidade aparece na complexidade, não na média do MI.
- **M7a** não muda: o P90 já estava na faixa Excelente, e os novos métodos não alteram o posto 90.

## 5. Limitações e próximos passos

- O teste de equivalência cobre a lógica de decisão do método; as consultas ao banco são dublês. A suíte do i-Educar, que exige PHP 8.5 e PostgreSQL, não foi executada com o patch.
- O maior método extraído, `_situacaoComponentePorNota` ($v(G) = 17$), ainda pode ser dividido.
- Os próximos candidatos, pela mesma métrica, são `getSituacaoFaltas` ($v(G) = 30$), `promover` (28) e `_updateNotaComponenteMedia` (26), todos em `Boletim.php`.
- O patch pode ser proposto ao projeto `portabilis/i-educar` acompanhado do teste de equivalência.

## 6. Reprodução

```bash
# No checkout do i-Educar, no commit avaliado
cd /caminho/i-educar
git checkout 7903a3efc7689942ee700007f86ed581023aad27
cp ieducar/modules/Avaliacao/Service/Boletim.php /tmp/Boletim.original.php
git apply /caminho/repositorio/docs/evidencias/melhoria/getSituacaoNotas.patch

# Teste de equivalência (50.000 cenários e autoteste)
php /caminho/repositorio/scripts/melhoria/teste_equivalencia.php \
  --original=/tmp/Boletim.original.php \
  --refatorado=ieducar/modules/Avaliacao/Service/Boletim.php \
  --casos=50000 --semente=2026 --autoteste

# Nova medição de M7a, M7b e M10
php /caminho/repositorio/scripts/evaluate-quality.php --path=. --evidence-dir=/tmp/depois
```
