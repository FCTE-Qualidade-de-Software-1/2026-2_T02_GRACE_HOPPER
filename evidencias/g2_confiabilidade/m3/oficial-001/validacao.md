# Validação da entrega M3 — issue #40

- Suíte principal: `junit.xml`, 30 testes, 457 asserções, zero erros, falhas ou skips; código de saída zero.
- DCNM: 30/30 × 100% = 100%; `summary.json` registra gate APROVADO, modo official e aceite da coleta verdadeiro.
- Rastreabilidade: os sete arquivos em `instrument/` foram comparados byte a byte com `scripts/avaliacao/m3/` no commit registrado em `environment.json`; todos correspondem. O manifesto também corresponde ao commit inicial `434cf17`.
- `python3 -m unittest discover -s scripts/avaliacao/m3 -p 'test_*.py'`: nove testes aprovados, saída zero.
- `bash scripts/docs/check_site.sh`: build estrito e verificações do site aprovados, saída zero. O build registra uma informação sobre âncora de custos PSM ausente, já presente na main, sem erro de compilação.
- `git diff --check -- . ':!evidencias/**'`: saída zero. Os logs brutos de evidências preservam espaços e quebras de linha produzidos pelo runner.
- A worktree do produto voltou limpa após a execução, com o arquivo legado restaurado.
- Testes legados complementares: dez erros de pré-requisito `StudentNotEnrolledInSchoolClass`, código de saída 2; classificados separadamente em `legacy-summary.json`, fora do denominador de M3.

Este registro valida a medição no universo de 30 casos. Não representa aprovação do fluxo completo do diário, dos demais gates ou revisão por pares do PR. O apontamento de horas e custo permanece pendente de validação do responsável.
