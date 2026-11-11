# M3 — DCNM: cálculo de notas e menções

Instrumentação da issue #40, organizada no mesmo diretório de avaliação usado por M1 e M2 no PR #52.

| Arquivo | Responsabilidade |
| :--- | :--- |
| `manifest.json` | Universo de 30 IDs, entradas, regras e resultados esperados do oráculo. |
| `manifest.sha256` | Digest de referência do manifesto, conferido antes de executar o produto. |
| `M3OracleTest.php` | Suíte Pest que chama o motor real e compara as saídas com o oráculo. |
| `run.py` | Verifica preparação e commit, executa a suíte e consolida as evidências por ID. |
| `compose.yml` | PHP 8.5, PostgreSQL 18 e Redis exclusivos, sem portas publicadas no host. |
| `php.sh` | Encaminha as chamadas PHP do executor ao container da M3. |
| `test_report.py` | Testes das regras de consolidação; não medem a qualidade do i-Educar. |

O hash detecta alteração em relação à referência registrada. A anterioridade do oráculo depende de versionar o instrumento e o manifesto antes da coleta oficial; o hash sozinho não comprova essa ordem.

## Executar

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

Cada rodada exige uma pasta de saída nova. A suíte injeta arquivos de teste no checkout descartável. Preparação completa, limitações e critérios estão em [Medição M3](../../../docs/medicao_m3_dcnm.md).

## Evidências

```text
evidencias/g2_confiabilidade/m3/<rodada>/
├── environment.json   # commits, versões, hashes, comandos e impedimentos
├── manifest.json      # cópia do universo usado
├── manifest.sha256    # referência conferida pelo executor
├── execution.txt      # stdout/stderr da suíte principal
├── junit.xml          # resultados do Pest, quando a execução o produzir
├── legacy.txt         # inspeção complementar, quando executada
├── results.csv        # esperado, obtido e status por ID
└── summary.json       # DCNM, anomalias e veredito do gate
```

O DCNM usa os 30 casos planejados como denominador. Aprovação exige 100%, evidência completa e execução válida. Falhas de preparação bloqueiam a comprovação do gate, sem demonstrar defeito no cálculo do produto. A pasta `preflight-local/` preserva uma tentativa anterior à reorganização; seu conteúdo histórico não foi reescrito.
