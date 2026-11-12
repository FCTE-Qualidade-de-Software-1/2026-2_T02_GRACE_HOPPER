# Plano de medição — M3: Notas e Menções (DCNM)

## Objetivo e universo

Esta entrega da issue #40 responde à Q2.1 e à H2.1 do [framework GQM](gqm_evaluation_framework.md#m3-determinismo-no-calculo-de-notas-e-mencoes-dcnm-gate-binario). O oráculo é uma regra pedagógica explícita e seu resultado previamente calculado, independente da implementação avaliada.

O manifesto v1.0 contém **30 IDs**, fixados antes da execução oficial, para o commit `7903a3efc7689942ee700007f86ed581023aad27` do i-Educar. Manifesto, suíte Pest e executor estão em `scripts/avaliacao/m3/` no repositório. O JSON é a fonte das entradas e saídas esperadas; não se recalcula o esperado usando funções do produto.

A organização segue o padrão adotado para M1/M2 no PR #52: instrumentação em `scripts/avaliacao/`, evidências por característica em `evidencias/` e documentação em `docs/`. Este documento é específico da M3 e complementa o plano geral de medição. A estrutura dos arquivos está descrita em `scripts/avaliacao/m3/README.md`.

O executor confere `manifest.sha256` antes de executar a suíte e copia essa referência para cada nova rodada. O hash detecta divergência do manifesto; a definição prévia do oráculo exige também seu versionamento anterior à execução oficial. A tentativa histórica em `preflight-local/` antecede essa verificação adicional e foi preservada sem alteração de conteúdo.

A Tabela 1 apresenta o universo do manifesto.

**Tabela 1 — Casos do oráculo M3 por família**

| IDs | Regra e entradas | Saídas esperadas, na ordem |
| :--- | :--- | :--- |
| A01–A04 | Média aritmética de quatro etapas: `[0,0,0,0]`, `[10,10,10,10]`, `[6,7,8,9]`, `[5,6,6,7]` | 0; 10; 7,5; 6 |
| P01–P03 | Notas `[4,8]`, pesos `[1,3]`; mesmas notas, pesos `[3,1]`; notas `[6,6]`, pesos `[1,3]` | 7; 5; 6 |
| R01–R02 | Recuperação por maior nota: `(4,8)`, `(7,3)` | 8; 7 |
| R03–R04 | Maior valor entre nota original e média com recuperação: `(4,8)`, `(7,3)` | 6; 7 |
| R05–R06 | Soma: nota 4 com recuperação 2; nota 4 sem recuperação (duplica a nota nesta modalidade) | 6; 8 |
| E01–E03 | `0,6 × média anual + 0,4 × exame`: `(4,4)`, `(5,7,5)`, `(5,10)` | 4; 6; 7 |
| N01–N04 | 5,4 para inteiro inferior; 5,5 para superior; 5,8 para decimal específico 5; média 5,99 truncada a uma casa sem tabela adicional | 5; 6; 5,5; 5,9 |
| C01–C09 | Entradas 0; 5,49; 5,50; 5,51; 6,50; 8; 8,01; 9,15; 10 | I; I; I; S; S; S; O; O; O |
| C10 | Média conceitual normalizada: soma 26 em quatro etapas | S (26/4 = 6,5) |

*Fonte: manifesto v1.0 da equipe, `scripts/avaliacao/m3/manifest.json`.*

A média ponderada divide a soma dos produtos nota × peso pela soma dos pesos. A tabela conceitual define I em `[0;5,50]`, S em `[5,51;8]` e O em `[8,01;10]`; os casos não normalizados usam duas casas de entrada. N01–N03 configuram ações explícitas na tabela numérica. Nos demais casos numéricos a tabela não transforma valores e a precisão final é uma casa decimal. A tolerância técnica de `1e-9` verifica ruído binário; não permite aceitar diferenças de centésimos ou décimos. Menções exigem igualdade exata.

A suíte utiliza o motor real de Boletim, fórmulas reais e tabelas reais. Fixtures e mocks fornecem matrícula, componente, regras e persistência. As fórmulas de média são acessadas por reflexão para isolar o cálculo sem duplicar a implementação; recuperação usa `calculateStageScore`, e arredondamento usa `arredondaNota`/`arredondaMedia`. Este recorte não comprova o fluxo completo de lançamento ou persistência no diário.

Excluem-se configurações municipais arbitrárias, recuperação por etapas específicas, validação de entradas inválidas, interface, concorrência e atomicidade. A aprovação é limitada ao universo pré-declarado.

## Critério e consolidação

$$
\mathrm{DCNM} = \frac{N_{\text{conformes}}}{N_{\text{planejados}}} \times 100\%
$$

- O denominador é sempre o manifesto, nunca a quantidade de testes encontrados pelo Pest.
- Falha, erro, skip, ausência de execução ou evidência deixam o caso não conforme.
- Duplicidade e IDs desconhecidos invalidam o aceite da execução.
- DCNM = 100% com universo não vazio, evidências completas e execução válida: **APROVADO**.
- Qualquer outro resultado: **BLOQUEADO**. Universo vazio é não mensurável.
- Reexecuções diagnósticas não contam como novos casos; uma nova rodada usa outra pasta de evidências.

Exemplo: 29/30 corresponde exatamente a `290/3%`, aproximadamente 96,6667%, e bloqueia M3. Falha de preparação com os 30 IDs ausentes registra 0/30 e gate não comprovado; não demonstra defeito nas fórmulas do produto.

## Preparação e execução reproduzível

1. Preparar uma cópia isolada e limpa do produto no commit exigido. Não trocar o commit da cópia de desenvolvimento existente.
2. Disponibilizar PHP 8.5, extensões exigidas pelo produto (incluindo BCMath), PostgreSQL 18 e banco exclusivo `testing`. Usar a configuração de testes e migrações do próprio i-Educar com dados sintéticos. Registrar versões e comandos de preparação junto às evidências. Nunca executar migrações contra banco compartilhado ou de produção.
3. Instalar as dependências de desenvolvimento com `composer install` a partir do lockfile desse commit. Não utilizar `composer update` nem reutilizar o vendor de outro commit.
4. Versionar os arquivos de `scripts/avaliacao/m3/` antes da rodada oficial. O executor recusa instrumento pendente de versionamento e produto em outro commit ou com alterações prévias.
5. Executar na raiz deste repositório, com um nome de pasta novo:

```bash
python scripts/avaliacao/m3/run.py --product /caminho/ieducar-isolado --output evidencias/g2_confiabilidade/m3/rodada-001
```

Se PHP estiver no contêiner, informar sua invocação, por exemplo `--php-command 'docker compose exec -T php php'`, ajustando o nome do serviço ao ambiente preparado. O serviço precisa acessar o diretório do produto. O executor injeta dois arquivos novos de teste na worktree e remove esses arquivos e o JUnit temporário ao terminar. A worktree precisa estar limpa no início de cada rodada; as evidências e uma cópia do instrumento usado ficam preservadas fora dela.

A execução integral dos 30 casos é uma suíte dedicada, sem interrupção na primeira falha. O executor preserva stdout/stderr, código de saída, relatório JUnit, manifesto usado, hashes SHA-256 do instrumento/lockfile e commits. `summary.json` e `results.csv` relacionam cada ID a esperado, obtido e status. Resultado obtido ausente em erro/skip permanece nulo.

Antes da suíte, o executor compara os hashes do Boletim, do lockfile, da suíte e do manifesto no runtime com os arquivos da worktree.

O responsável deve anexar também o inventário real do banco e do ambiente, o comando de migração e a identificação das fixtures. Não publicar credenciais, dados pessoais ou arquivos `.env`.

## Inspeção complementar do legado

No commit fixado, `NotaSituacaoCommon.php` registra cinco cenários Pest, todos com `markTestSkipped()`. São cenários de situação escolar com médias previamente fornecidas, não suficientes para provar o cálculo das médias.

Após a suíte M3, o executor remove temporariamente esses skips somente da cópia isolada, executa os testes numéricos e conceituais e restaura o arquivo em `finally`. O log e código de saída ficam separados em `legacy.txt` e `environment.json`. O executor também preserva `legacy-junit.xml`, a classificação individual em `legacy-summary.json` e o patch exato em `legacy-reactivation.patch`. Os cinco cenários são registrados uma vez na suíte numérica e outra na conceitual, totalizando dez testes. A revisão identificou IDs fixos de componentes e matrícula sem vínculo de turma exigido por `App_Model_IedFinder::getRegraAvaliacaoPorMatricula`; os dez casos interrompem em `StudentNotEnrolledInSchoolClass`, antes da comparação da situação esperada. A validação desses cenários requer atualização de suas fixtures em uma entrega separada. Não se declara aprovação desse fluxo nem defeito matemático a partir desses erros. Falhas de compatibilidade devem ser documentadas; não se altera o produto nem o resultado esperado para obter aprovação. Esses cenários complementares não entram no denominador dos 30 casos.

## Estado das evidências e aceite

O ambiente local foi preparado na worktree `../Projeto/i-educar-m3`, fixada no commit obrigatório. O Compose dedicado está em `scripts/avaliacao/m3/compose.yml`: PHP 8.5, PostgreSQL 18, Redis e banco exclusivo `testing`, sem portas publicadas. As dependências foram instaladas com `composer install` pelo lockfile, sem atualização de versões. Logs de instalação, migrações, versão do PHP e inventário do banco estão em `evidencias/g2_confiabilidade/m3/preparacao/`.

A Tabela 2 conserva o histórico das tentativas e diagnósticos.

**Tabela 2 — Histórico de execução da M3**

| Rodada | Resultado | Interpretação |
| :--- | :--- | :--- |
| `preflight-local/` | Nenhum caso executado; commit incorreto | Impedimento histórico, preservado. |
| `rodada-001/` | 30 erros antes das asserções | Erro do instrumento: `qtdCasasDecimais` não consta dos defaults aceitos pelo setter do helper legado. Não é evidência de defeito no cálculo do produto. |
| `diagnostico-002/` | 29/30 conformes | C10 recebeu zero etapas da fixture, embora seu manifesto declare quatro. Configuração incompleta da suíte. |
| `diagnostico-003/` | **30/30 conformes, 100%, 457 asserções** | Precisão configurada no modelo e quatro etapas fornecidas conforme o manifesto. Gate técnico aprovado; **sem aceite oficial**, pois o instrumento corrigido ainda não foi versionado. |
| `diagnostico-004/` | **30/30 conformes, 100%, 457 asserções** | Repetição pelo atalho `run_local.py`, com saída ao vivo e limpeza dos arquivos temporários. Resultado técnico confirmado; sem aceite oficial. |

*Fonte: logs e relatórios em `evidencias/g2_confiabilidade/m3/`.*

O manifesto e as saídas esperadas não foram alterados nessas correções. Os helpers legados geram avisos de depreciação do PHPUnit nos 30 testes; a última rodada terminou com código zero e sem falha, erro ou skip no JUnit. A inspeção complementar do legado registra dez erros `StudentNotEnrolledInSchoolClass` (aluno não enturmado), decorrentes de pré-requisito ausente nas fixtures; esses testes não entram nos 30 casos nem sustentam aprovação do fluxo completo.

Para acompanhar a repetição no terminal do VS Code, executar na raiz deste repositório:

```bash
python3 scripts/avaliacao/m3/run_local.py
```

O atalho sempre usa modo diagnóstico, aceita alterações locais sem commit e cria uma pasta nova por execução. `technical_gate` registra o resultado técnico; `official_acceptance` permanece falso e `gate` permanece bloqueado. A coleta oficial exige posterior versionamento dos instrumentos e nova execução sem `--diagnostic`; nenhum novo commit é necessário para repetir o diagnóstico.

A implementação deve ser validada com:

```bash
python -m unittest discover -s scripts/avaliacao/m3 -p 'test_*.py'
bash scripts/docs/check_site.sh
```

Os testes do consolidador cobrem aprovação integral, falha, skip, erro, casos ausentes, IDs duplicados/desconhecidos, universo vazio e processo com saída não zero. Eles não substituem a suíte pedagógica.

O aceite final exige execução real dos 30 IDs no commit obrigatório, ambiente inventariado, oráculo versionado antes da rodada, evidência completa, cálculo do DCNM e veredito explícito. Registrar na issue horas efetivas, custo, datas, commit da entrega e caminhos das evidências. Corrigir o produto é uma entrega separada: a medição pode ser concluída com gate bloqueado quando evidenciar falhas reais.
