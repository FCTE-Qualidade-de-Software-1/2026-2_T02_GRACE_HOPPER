# Compatibilidade — M1 (TINCR) e M2 (CEI)

**Issues:** [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38) e [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39) · **PR:** [#52](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/52)
**Responsável:** Ítalo Alves Sampaio de Oliveira
**Milestone:** M5
**Fase ISO/IEC 25040:2024:** 4 (Execução da Avaliação)
**Característica ISO/IEC 25010:2023:** Compatibilidade (Coexistência e Interoperabilidade)
**Commit do produto:** `7903a3efc7689942ee700007f86ed581023aad27`
**Evidências:** `evidencias/g1_compatibilidade/`

## 1. Resumo

| Métrica | Resultado | Nível | Hipótese |
| :--- | :--- | :---: | :--- |
| `M1` — TINCR | $16/16 = 100{,}0\%$ | Excelente ($S = 4$) | H1.1 (TINCR $\ge 85\%$): **confirmada** |
| `M2` — CEI | $9/10 = 90{,}0\%$ | Bom ($S = 3$) | H1.2 (CEI $\ge 85\%$): **confirmada**; falha no envelope de erro do `E08` |

$\text{IQC}_{\text{Comp}} = (4 \times 1{,}0 + 3 \times 1{,}0) / 2{,}0 = 3{,}50$, a maior nota entre as quatro características avaliadas.

*Fonte: Elaborado pelos autores a partir de `evidencias/g1_compatibilidade/` e da Seção 6 do [Plano de Medição](../plano_medicao_testes.md#6-resultados-da-execucao-da-caracteristica-compatibilidade-g1-issues-38-e-39).*

Esta página registra a execução empírica de **M1 (TINCR)** e **M2 (CEI)** sobre o commit congelado `7903a3efc7689942ee700007f86ed581023aad27`. Todos os valores decorrem dos logs e relatórios versionados em `evidencias/g1_compatibilidade/`; nenhum valor foi arbitrado.

## 2. Ambiente Docker Provisionado (Issue #38)

O `docker-compose.yml` da raiz passou a construir a imagem PHP a partir de `docker/php` do checkout oficial (variável `IEDUCAR_SRC`) e a parametrizar todos os recursos compartilháveis por variáveis. O código-fonte do i-Educar não foi alterado. As duas instâncias usam os arquivos `config/instancia-a.env` e `config/instancia-b.env`.

```bash
git clone https://github.com/portabilis/i-educar.git ../_work/i-educar
git -C ../_work/i-educar checkout 7903a3efc7689942ee700007f86ed581023aad27
bash scripts/infra/gerar_env_fonte.sh config/instancia-a.env
docker compose --env-file config/instancia-a.env up -d --build
docker compose --env-file config/instancia-a.env exec -e COMPOSER_NO_SECURITY_BLOCKING=1 php composer install
docker compose --env-file config/instancia-a.env exec php php artisan migrate --force
docker compose --env-file config/instancia-a.env exec php php artisan db:seed --force
docker compose --env-file config/instancia-a.env exec php php artisan db:seed --class=DemoSeeder --force
```

Resultado: migrações concluídas (exit 0), seeds padrão e `DemoSeeder` aplicados (210 matrículas no ano de 2026) e `GET /api/version` retornando `{"entity":"i-Educar","version":"2.12.0"}` nas duas instâncias.

**Tabela 1 — Inventário de recursos compartilháveis e resultado do teste de coexistência (M1)**

| Id | Recurso compartilhável | Variável que o isola | Instância A | Instância B | Colisão? | Isolável |
| :-: | :--- | :--- | :--- | :--- | :---: | :---: |
| R1 | Porta HTTP do host | `DOCKER_NGINX_PORT` | `8080` | `8081` | Não | Sim |
| R2 | Porta HTTPS do host | `DOCKER_NGINX_SSL_PORT` | `8443` | `8444` | Não | Sim |
| R3 | Porta PostgreSQL do host | `DOCKER_POSTGRES_PORT` | `5432` | `5433` | Não | Sim |
| R4 | Porta Redis do host | `DOCKER_REDIS_PORT` | `6379` | `6380` | Não | Sim |
| R5 | `container_name` do serviço `php` | `INSTANCE_NAME` | `ieducar-a-php` | `ieducar-b-php` | Não | Sim |
| R6 | `container_name` do serviço `fpm` | `INSTANCE_NAME` | `ieducar-a-fpm` | `ieducar-b-fpm` | Não | Sim |
| R7 | `container_name` do serviço `nginx` | `INSTANCE_NAME` | `ieducar-a-nginx` | `ieducar-b-nginx` | Não | Sim |
| R8 | `container_name` do serviço `postgres` | `INSTANCE_NAME` | `ieducar-a-postgres` | `ieducar-b-postgres` | Não | Sim |
| R9 | `container_name` do serviço `redis` | `INSTANCE_NAME` | `ieducar-a-redis` | `ieducar-b-redis` | Não | Sim |
| R10 | Banco de dados (`DB_DATABASE`) | `DB_DATABASE` | `ieducar` | `ieducar_b` | Não | Sim |
| R11 | Usuário do banco (`DB_USERNAME`) | `DB_USERNAME` | `ieducar` | `ieducar_b` | Não | Sim |
| R12 | Prefixo de chaves no Redis | `REDIS_PREFIX` | `ieducar-a-` | `ieducar-b-` | Não | Sim |
| R13 | Volume nomeado do PostgreSQL | `COMPOSE_PROJECT_NAME` | `ieducar-a_postgres` | `ieducar-b_postgres` | Não | Sim |
| R14 | Rede Docker | `COMPOSE_PROJECT_NAME` | `ieducar-a_default` | `ieducar-b_default` | Não | Sim |
| R15 | Diretório de armazenamento (`storage/`, `.env`) | `IEDUCAR_SRC` | `.../i-educar` | `.../i-educar-b` | Não | Sim |
| R16 | Tag da imagem de aplicação | `INSTANCE_NAME` | `ieducar-a-php:8.5` | `ieducar-b-php:8.5` | Não | Sim |

*Fonte: `evidencias/g1_compatibilidade/m1_tincr.log` (comandos e saídas brutas). Elaborado pelos autores.*

Verificações complementares registradas no log: (i) um marcador gravado no banco `ieducar_b` da instância B não existe no banco da instância A; (ii) a chave de cache gravada pela aplicação aparece como `ieducar-a-ieducarm1_probe` no Redis de A e `ieducar-b-ieducarm1_probe` no Redis de B, confirmando o prefixo por instância; (iii) as duas instâncias responderam simultaneamente nas portas `8080` e `8081`.

## 3. Cálculo de M1 (TINCR) e Avaliação da Hipótese H1.1

$$
\text{TINCR} = \dfrac{N_{\text{isoláveis}}}{N_{\text{identificados}}} \times 100\% = \dfrac{16}{16} \times 100\% = 100{,}0\%
$$

- **Nível:** Excelente ($S = 4$). **H1.1 (TINCR $\ge 85\%$): confirmada.**
- **Linha de base do compose oficial sem parametrização** (`evidencias/g1_compatibilidade/m1_baseline_upstream.log`): ao subir uma segunda instância com o `docker-compose.yml` do upstream, a criação falhou com `Conflict. The container name "/ieducar-redis" is already in use`, mesmo alterando as portas por variável. Considerando o compose do upstream como publicado (19 recursos: 4 portas, 7 `container_name`, 3 variáveis de `.env`, 3 volumes, 1 rede e 1 bind mount do código), apenas 11 são isoláveis por variável de ambiente isoladamente, o que resulta em $11/19 = 57{,}9\%$ (nível Crítico). Os 8 restantes (7 `container_name` e o bind mount `./`) exigem editar o arquivo de composição (`docker-compose.override.yml`, previsto no `INSTALL.md` do upstream). Como o critério de M1 admite "variável de ambiente ou arquivo de configuração" e nenhum código-fonte foi alterado, o valor oficial adotado é **100%**, com a ressalva de que a hipótese H1.1 se confirma somente após a substituição dos nomes fixos de container por variáveis.
- **Escopo do inventário:** foram considerados os serviços `php`, `fpm`, `nginx`, `postgres` e `redis`. Os serviços `horizon` e `pest` do upstream não foram instanciados nesta medição.

## 4. Achados e Ameaças à Validade do Ambiente (Issue #38)

1. **Bloqueio do Composer por *security advisories*:** o `composer install` do `composer.lock` do commit fixo falha porque 18 pacotes constam em avisos de segurança (PKSA) atuais. Foi usada a variável `COMPOSER_NO_SECURITY_BLOCKING=1`, restrita ao ambiente isolado de laboratório; ao final foram reportados 12 avisos em 8 pacotes (`composer audit`). Não foi alterado nenhum arquivo versionado do i-Educar.
2. **`set-permissions` do `composer new-install`:** o `chmod` falha em bind mount NTFS (`Operation not permitted`); as demais etapas do script (`key:generate`, `storage:link`, `migrate`) foram executadas manualmente.
3. **Configuração lida do `.env` do checkout:** o `php-fpm` lê a configuração do `.env` do checkout, razão pela qual `scripts/infra/gerar_env_fonte.sh` gera esse arquivo por instância a partir do `.env.example` oficial.
4. **Chaves de API definidas no banco:** `API_ACCESS_KEY` e `API_SECRET_KEY` do `.env` são sobrescritas pela tabela `settings` (migração `populate_settings_table`, valores padrão `ieducar-access-key` e `ieducar-secret-key`). Os testes de M2 usam esses valores públicos do upstream.
5. **Limitação:** a medição de M1 foi feita em um único host Windows com Docker Desktop; a ausência de conflito em outros hosts não é inferida.

## 5. Contratos e Resultados de M2 (CEI — Issue #39)

**Congelamento prévio.** Os contratos JSON Schema (`contratos_json_schema.json`) e o manifesto de endpoints (`manifesto_endpoints.json`) em `evidencias/g1_compatibilidade/m2_contratos/` foram escritos antes da primeira execução; seus hashes SHA-256 foram registrados em `manifesto.sha256` (carimbo `congelado_em.txt`, `2026-11-11T16:45:08-03:00`) e o executor `scripts/avaliacao/m2_cei.py` aborta se qualquer hash divergir. Não há documentação oficial de contrato para esses endpoints; os esquemas foram derivados de `MatriculaController.php`, `DiarioApiController.php`, `ApiCoreController.php` e dos controllers REST de `routes/api.php`.

**Universo avaliado.** Foram congelados 10 endpoints de leitura dos módulos de Matrícula/Enturmação e Diário/Notas. Endpoints de escrita (`POST` de nota, `DELETE`) ficaram fora do universo para não alterar a base de homologação; a cobertura de M2 refere-se, portanto, a operações de consulta.

**Regras pré-registradas.** C1: HTTP 200 e `Content-Type: application/json`. C2: corpo aderente ao JSON Schema. C3: duas requisições inválidas (P1, parâmetro obrigatório ausente; P2, credencial incorreta) devem retornar status inferior a 500, `application/json` e erro estruturado conforme o esquema de erro do endpoint. Endpoints REST sem parâmetro obrigatório (E09, E10) têm apenas a sonda P2.

**Tabela 2 — Relatório de conformidade por endpoint (M2)**

| Id | Endpoint | Autenticação | C1 | C2 | C3 | Conforme |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: |
| E01 | `GET /module/Api/Matricula` `resource=matricula` | `access_key` | Sim | Sim | Sim | Sim |
| E02 | `GET /module/Api/Matricula` `resource=matriculas` | `access_key` | Sim | Sim | Sim | Sim |
| E03 | `GET /module/Api/Matricula` `resource=matriculas-escola` | `access_key` | Sim | Sim | Sim | Sim |
| E04 | `GET /module/Api/Matricula` `resource=frequencia` | `access_key` | Sim | Sim | Sim | Sim |
| E05 | `GET /module/Api/Matricula` `resource=matricula-search` | `access_key` | Sim | Sim | Sim | Sim |
| E06 | `GET /module/Api/Matricula` `resource=movimentacao-enturmacao` | `access_key` | Sim | Sim | Sim | Sim |
| E07 | `GET /module/Api/Matricula` `resource=matriculas-dependencia` | `access_key` | Sim | Sim | Sim | Sim |
| E08 | `GET /module/Avaliacao/DiarioApi` `resource=matriculas` | sessão | Sim | Sim | **Não** | **Não** |
| E09 | `GET /api/registration` | Bearer (Sanctum) | Sim | Sim | Sim | Sim |
| E10 | `GET /api/situation` | Bearer (Sanctum) | Sim | Sim | Sim | Sim |

*Fonte: `evidencias/g1_compatibilidade/m2_cei_report.json` e `m2_cei_execucao.log`. Elaborado pelos autores.*

$$
\text{CEI} = \dfrac{N_{\text{endpoints conformes}}}{N_{\text{endpoints testados}}} \times 100\% = \dfrac{9}{10} \times 100\% = 90{,}0\%
$$

- **Nível:** Bom ($S = 3$, faixa $[85\%, 100\%)$). **H1.2 (CEI $\ge 85\%$): confirmada.**
- **Falha de E08:** a requisição sem sessão válida retorna `401` com o corpo Laravel `{"message":"Unauthenticated."}`, enquanto as demais respostas de erro do mesmo recurso usam o envelope legado (`msgs` e `any_error_msg`). O contrato congelado previa o envelope legado, portanto o endpoint foi reprovado em C3. O resultado não foi reclassificado após a execução; a coexistência de dois formatos de erro no mesmo endpoint é o achado de interoperabilidade.
- **Observações sem efeito na pontuação:** (i) sem o cabeçalho `Accept: application/json`, a mesma chamada a E08 sem sessão redireciona para a página HTML de login (o executor envia o cabeçalho); (ii) E04 sem o parâmetro `id` devolve em JSON a mensagem bruta de exceção SQL (`SQLSTATE[42883]`) com `APP_DEBUG=true`, o que a torna estruturada porém expõe detalhes internos; (iii) a resposta válida de E08 retornou lista `matriculas` vazia para o recorte do seed, aderente ao esquema, mas sem exercitar os campos internos dos itens.
- **Ameaça à validade:** com 10 endpoints, cada endpoint vale 10 pontos percentuais; um único endpoint não conforme é suficiente para mudar o nível.

## 6. Como Reproduzir

```bash
bash scripts/avaliacao/m1_coexistencia.sh > evidencias/g1_compatibilidade/m1_tincr.log
python3 -m venv .venv-m2 && .venv-m2/bin/pip install jsonschema
.venv-m2/bin/python scripts/avaliacao/m2_cei.py --token "$TOKEN_SANCTUM_LAB"
```
