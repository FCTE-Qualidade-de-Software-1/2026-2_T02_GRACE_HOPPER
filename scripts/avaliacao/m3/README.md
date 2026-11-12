# M3 — DCNM: cálculo de notas e menções

Instrumentação da issue #40, organizada no mesmo diretório de avaliação usado por M1 e M2 no PR #52.

| Arquivo | Responsabilidade |
| :--- | :--- |
| `manifest.json` | Universo de 30 IDs, entradas, regras e resultados esperados do oráculo. |
| `manifest.sha256` | Digest de referência do manifesto, conferido antes de executar o produto. |
| `M3OracleTest.php` | Suíte Pest que chama o motor real e compara as saídas com o oráculo. |
| `run.py` | Verifica preparação e commit, executa a suíte e consolida as evidências por ID. |
| `run_local.py` | Repete a medição no Docker local, sempre em modo diagnóstico. |
| `compose.yml` | PHP 8.5, PostgreSQL 18 e Redis exclusivos, sem portas publicadas no host. |
| `php.sh` | Encaminha as chamadas PHP do executor ao container da M3. |
| `test_report.py` | Testes das regras de consolidação; não medem a qualidade do i-Educar. |

O hash detecta alteração em relação à referência registrada. A anterioridade do oráculo depende de versionar o instrumento e o manifesto antes da coleta oficial; o hash sozinho não comprova essa ordem.

## Executar

Com o ambiente local já preparado, na raiz do repositório:

```bash
python3 scripts/avaliacao/m3/run_local.py
```

Esse atalho usa a worktree irmã `../Projeto/i-educar-m3`, mostra a saída ao vivo e cria uma pasta de evidências com data/hora. Outro caminho pode ser informado com `--product`. Não faz commits. O modo diagnóstico admite instrumentos modificados, preserva uma cópia dos arquivos usados e nunca concede aceite oficial: confira `technical_gate`, `execution_mode` e `official_acceptance` no relatório. O `gate` permanece bloqueado para a entrega oficial até uma coleta com instrumento versionado.

Preparação do laboratório, na raiz deste repositório (substitua o caminho da worktree):

```bash
export M3_PRODUCT_DIR=/caminho/ieducar-isolado
docker compose -f scripts/avaliacao/m3/compose.yml up -d --build
docker compose -f scripts/avaliacao/m3/compose.yml exec -T php composer install --no-interaction --prefer-dist
docker compose -f scripts/avaliacao/m3/compose.yml exec -T php php artisan key:generate --force
docker compose -f scripts/avaliacao/m3/compose.yml exec -T php php artisan migrate --force
```

O Compose fixa `DB_DATABASE=testing` e usa um volume exclusivo do projeto `ieducar-m3`. As credenciais declaradas são somente do laboratório local. A worktree recebe seu próprio `.env` pelo script de instalação do produto. Não executar `composer update`.

Para usar os containers na execução abaixo, acrescente `--php-command 'bash /caminho/absoluto/deste/repositorio/scripts/avaliacao/m3/php.sh'`. O executor mostra a saída da suíte principal ao vivo e também a grava em `execution.txt`.

Na raiz do repositório, após preparar o checkout isolado e versionar o instrumento:

```bash
python3 scripts/avaliacao/m3/run.py \
  --product /caminho/ieducar-isolado \
  --output evidencias/g2_confiabilidade/m3/rodada-001
```

Cada rodada exige uma pasta de saída nova. A suíte injeta arquivos de teste no checkout isolado e remove seus próprios arquivos temporários ao terminar; uma cópia do instrumento usado fica em `instrument/` nas evidências. Preparação completa, limitações e critérios estão em [Medição M3](../../../docs/fase-4/medicao_m3_dcnm.md).

## Evidências

```text
evidencias/g2_confiabilidade/m3/<rodada>/
├── environment.json   # commits, versões, hashes, comandos e impedimentos
├── manifest.json      # cópia do universo usado
├── manifest.sha256    # referência conferida pelo executor
├── execution.txt      # stdout/stderr da suíte principal
├── junit.xml          # resultados do Pest, quando a execução o produzir
├── legacy.txt         # inspeção complementar, quando executada
├── legacy-junit.xml   # resultados estruturados dos testes legados
├── legacy-summary.json # classificação das falhas legadas; fora do DCNM
├── legacy-reactivation.patch # remoção temporária dos skips, restaurada ao terminar
├── results.csv        # esperado, obtido e status por ID
└── summary.json       # DCNM, anomalias e veredito do gate
```

O DCNM usa os 30 casos planejados como denominador. Aprovação exige 100%, evidência completa e execução válida. Falhas de preparação bloqueiam a comprovação do gate, sem demonstrar defeito no cálculo do produto. A pasta `preflight-local/` preserva uma tentativa anterior à reorganização; seu conteúdo histórico não foi reescrito.

Antes da suíte, o executor compara no host e no runtime os hashes do lockfile, do Boletim, da suíte e do manifesto injetados. Isso impede uma coleta sobre um volume diferente da worktree selecionada. Os testes legados são relatados separadamente: erros de pré-requisito como aluno sem enturmação não são convertidos em sucesso nem classificados como erro matemático.
