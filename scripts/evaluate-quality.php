#!/usr/bin/env php
<?php
/**
 * Motor de Avaliação Estática de Qualidade de Software — i-Educar 2.12
 * Disciplina: Qualidade de Software 1 (FGA0315) - UnB / FGA
 * Framework GQM: M7a (CC P90), M7b (CC Max), M8 (DSPM), M9 (IFDL), M10 (MI) e M11 (TTAE)
 * Issue #11: Planejamento das Ferramentas de Análise Estática e Motor PHP
 * Issue #43: Extração de M7a, M7b e M10 por callable (Fase 4)
 *
 * NOTA METODOLÓGICA (Fase 4 — ISO/IEC 25040:2024):
 * M7a, M7b e M10 são calculados por análise léxica (token_get_all) sobre os 4 arquivos de produção
 * do manifesto congelado. M8, M9 e M11 permanecem pendentes neste instrumento (Issue #44).
 * Nenhum valor é arbitrado: sem os arquivos do manifesto, as métricas ficam não mensuráveis.
 *
 * Uso:
 *   php scripts/evaluate-quality.php --path=/caminho/i-educar [--json] [--commit=<sha>] [--evidence-dir=<dir>]
 */

declare(strict_types=1);

const VERSAO_INSTRUMENTO = '2.0.0';

/** Manifesto congelado de arquivos de produção (GQM, M7a/M7b/M10). */
const ARQUIVOS_ESCOPO = [
    'app/Services/RegistrationService.php',
    'ieducar/modules/Avaliacao/Views/DiarioApiController.php',
    'ieducar/modules/Avaliacao/Views/DiarioController.php',
    'ieducar/modules/Avaliacao/Service/Boletim.php',
];

/**
 * Extrai os callables concretos de um arquivo PHP e calcula, para cada um,
 * v(G), as contagens de Halstead, o volume HV, o LOC lógico e o MI normalizado.
 */
final class AnalisadorCallables
{
    /** Pontos de decisão contados em v(G) (além do ternário "?", tratado à parte). */
    private const TOKENS_DECISAO = [
        T_IF, T_ELSEIF, T_FOR, T_FOREACH, T_WHILE, T_CASE, T_CATCH,
        T_BOOLEAN_AND, T_BOOLEAN_OR, T_LOGICAL_AND, T_LOGICAL_OR, T_COALESCE,
    ];

    /** Tokens contados como operandos de Halstead; os demais tokens significativos são operadores. */
    private const TOKENS_OPERANDO = [
        T_VARIABLE, T_STRING, T_NAME_QUALIFIED, T_NAME_FULLY_QUALIFIED, T_NAME_RELATIVE,
        T_LNUMBER, T_DNUMBER, T_CONSTANT_ENCAPSED_STRING, T_ENCAPSED_AND_WHITESPACE,
        T_NUM_STRING, T_STRING_VARNAME, T_LINE, T_FILE, T_DIR, T_CLASS_C, T_FUNC_C,
        T_METHOD_C, T_NS_C, T_TRAIT_C,
    ];

    /** Tokens ignorados em todas as contagens. */
    private const TOKENS_IGNORADOS = [
        T_WHITESPACE, T_COMMENT, T_DOC_COMMENT, T_OPEN_TAG, T_OPEN_TAG_WITH_ECHO, T_CLOSE_TAG, T_INLINE_HTML,
    ];

    /** Palavras-chave que abrem uma estrutura de controle (somadas ao LOC lógico). */
    private const TOKENS_ESTRUTURA = [
        T_IF, T_ELSEIF, T_ELSE, T_FOR, T_FOREACH, T_WHILE, T_DO, T_SWITCH, T_CASE, T_DEFAULT,
        T_TRY, T_CATCH, T_FINALLY,
    ];

    /** @return array{callables: list<array<string,mixed>>, excluidos: list<array<string,mixed>>} */
    public function analisarArquivo(string $caminho, string $rotulo): array
    {
        $tokens = token_get_all((string) file_get_contents($caminho), TOKEN_PARSE);
        $total = count($tokens);
        $callables = [];
        $excluidos = [];
        $escopos = []; // pilha de [nome, profundidade do corpo]
        $profundidade = 0;
        $tipoPendente = null;

        for ($i = 0; $i < $total; $i++) {
            $t = $tokens[$i];
            $id = is_array($t) ? $t[0] : null;

            if (in_array($id, [T_CLASS, T_INTERFACE, T_TRAIT, T_ENUM], true)
                && !$this->anteriorSignificativo($tokens, $i, [T_DOUBLE_COLON, T_NEW])) {
                $nome = $this->proximoSignificativo($tokens, $i);
                $tipoPendente = (is_array($nome) && $nome[0] === T_STRING) ? $nome[1] : null;
                continue;
            }

            if ($t === '{' || in_array($id, [T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES], true)) {
                $profundidade++;
                if ($tipoPendente !== null) {
                    $escopos[] = [$tipoPendente, $profundidade];
                    $tipoPendente = null;
                }
                continue;
            }
            if ($t === '}') {
                if ($escopos && end($escopos)[1] === $profundidade) {
                    array_pop($escopos);
                }
                $profundidade--;
                continue;
            }

            if ($id !== T_FUNCTION) {
                continue;
            }

            // Closures (function (...)) pertencem ao callable que as contém.
            $j = $this->indiceProximoSignificativo($tokens, $i);
            if ($j !== null && $tokens[$j] === '&') {
                $j = $this->indiceProximoSignificativo($tokens, $j);
            }
            if ($j === null || !is_array($tokens[$j])) {
                continue;
            }
            $nome = $tokens[$j][1];
            $linha = $tokens[$i][2];
            $classe = $escopos ? end($escopos)[0] : null;
            $simbolo = ($classe !== null ? $classe . '::' : '') . $nome;

            // Localiza o corpo: ";" antes de "{" indica método abstrato ou de interface.
            $k = $j;
            $parenteses = 0;
            while ($k < $total) {
                $tk = $tokens[$k];
                if ($tk === '(') {
                    $parenteses++;
                } elseif ($tk === ')') {
                    $parenteses--;
                } elseif ($parenteses === 0 && ($tk === '{' || $tk === ';')) {
                    break;
                }
                $k++;
            }
            if ($k >= $total || $tokens[$k] === ';') {
                $excluidos[] = ['arquivo' => $rotulo, 'simbolo' => $simbolo, 'linha' => $linha, 'motivo' => 'declaração sem corpo (abstrata ou de interface)'];
                $i = $k;
                continue;
            }

            $inicioCorpo = $k;
            $fim = $this->fechamento($tokens, $inicioCorpo);
            $callables[] = $this->medir($tokens, $i, $inicioCorpo, $fim) + [
                'arquivo' => $rotulo,
                'classe' => $classe,
                'callable' => $nome,
                'simbolo' => $simbolo,
                'linha_inicio' => $linha,
                'linha_fim' => $this->linhaDoToken($tokens, $fim),
            ];
            // Callables aninhados (por exemplo, métodos de classes anônimas) ficam no callable externo.
            $i = $fim;
        }

        return ['callables' => $callables, 'excluidos' => $excluidos];
    }

    /** @return array<string,mixed> */
    private function medir(array $tokens, int $inicio, int $inicioCorpo, int $fim): array
    {
        $cc = 1;
        $lloc = 1; // a própria declaração do callable
        $parenteses = 0;
        $operadores = [];
        $operandos = [];
        $anterior = null;

        for ($i = $inicio; $i <= $fim; $i++) {
            $t = $tokens[$i];
            $id = is_array($t) ? $t[0] : null;
            if ($id !== null && in_array($id, self::TOKENS_IGNORADOS, true)) {
                continue;
            }
            $texto = is_array($t) ? $t[1] : $t;
            $noCorpo = $i > $inicioCorpo;

            // Halstead: parênteses, colchetes e chaves contam uma vez, na abertura.
            if (!in_array($texto, [')', ']', '}'], true)) {
                if ($id !== null && in_array($id, self::TOKENS_OPERANDO, true)) {
                    $operandos[] = $texto;
                } else {
                    $operadores[] = $id !== null ? strtolower($texto) : $texto;
                }
            }

            if ($noCorpo) {
                if ($id === T_MATCH) {
                    $cc += $this->bracosMatch($tokens, $i);
                }
                if ($id !== null && in_array($id, self::TOKENS_DECISAO, true)) {
                    $cc++;
                } elseif ($texto === '?' && !in_array($anterior, ['(', ',', ':'], true)) {
                    $cc++; // ternário; "?" após "(", "," ou ":" é tipo anulável
                }

                if ($texto === '(') {
                    $parenteses++;
                } elseif ($texto === ')') {
                    $parenteses--;
                } elseif ($texto === ';' && $parenteses === 0) {
                    $lloc++;
                }
                if ($id !== null && in_array($id, self::TOKENS_ESTRUTURA, true)) {
                    $lloc++;
                }
            }
            $anterior = $texto;
        }

        $n1 = count(array_unique($operadores));
        $n2 = count(array_unique($operandos));
        $N1 = count($operadores);
        $N2 = count($operandos);
        $vocabulario = $n1 + $n2;
        $comprimento = $N1 + $N2;
        $hv = $vocabulario > 1 ? $comprimento * log($vocabulario, 2) : 0.0;

        $mi = null;
        if ($hv > 0 && $lloc > 0) {
            $bruto = (171 - 5.2 * log($hv) - 0.23 * $cc - 16.2 * log($lloc)) / 171 * 100;
            $mi = min(100.0, max(0.0, $bruto));
        }

        return [
            'cc' => $cc,
            'halstead' => ['n1' => $n1, 'n2' => $n2, 'N1' => $N1, 'N2' => $N2],
            'hv' => round($hv, 4),
            'lloc' => $lloc,
            'mi' => $mi === null ? null : round($mi, 4),
        ];
    }

    /** Braços de um match, exceto default: cada braço é um ponto de decisão, como um case. */
    private function bracosMatch(array $tokens, int $iMatch): int
    {
        $abertura = $iMatch;
        while ($tokens[$abertura] !== '{') {
            $abertura++;
        }
        $fim = $this->fechamento($tokens, $abertura);
        $bracos = 0;
        $temDefault = false;
        $aninhamento = 0;
        for ($i = $abertura + 1; $i < $fim; $i++) {
            $t = $tokens[$i];
            if (in_array($t, ['(', '[', '{'], true) || (is_array($t) && in_array($t[0], [T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES], true))) {
                $aninhamento++;
            } elseif (in_array($t, [')', ']', '}'], true)) {
                $aninhamento--;
            } elseif ($aninhamento === 0 && is_array($t) && $t[0] === T_DOUBLE_ARROW) {
                $bracos++;
            } elseif ($aninhamento === 0 && is_array($t) && $t[0] === T_DEFAULT) {
                $temDefault = true;
            }
        }
        return $bracos - ($temDefault ? 1 : 0);
    }

    private function fechamento(array $tokens, int $abertura): int
    {
        $nivel = 0;
        $total = count($tokens);
        for ($i = $abertura; $i < $total; $i++) {
            $t = $tokens[$i];
            if ($t === '{' || (is_array($t) && in_array($t[0], [T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES], true))) {
                $nivel++;
            } elseif ($t === '}') {
                $nivel--;
                if ($nivel === 0) {
                    return $i;
                }
            }
        }
        throw new RuntimeException('Chave de fechamento não encontrada.');
    }

    private function indiceProximoSignificativo(array $tokens, int $i): ?int
    {
        for ($j = $i + 1, $total = count($tokens); $j < $total; $j++) {
            if (!(is_array($tokens[$j]) && in_array($tokens[$j][0], self::TOKENS_IGNORADOS, true))) {
                return $j;
            }
        }
        return null;
    }

    private function proximoSignificativo(array $tokens, int $i): mixed
    {
        $j = $this->indiceProximoSignificativo($tokens, $i);
        return $j === null ? null : $tokens[$j];
    }

    private function anteriorSignificativo(array $tokens, int $i, array $ids): bool
    {
        for ($j = $i - 1; $j >= 0; $j--) {
            $t = $tokens[$j];
            if (is_array($t) && in_array($t[0], self::TOKENS_IGNORADOS, true)) {
                continue;
            }
            return is_array($t) && in_array($t[0], $ids, true);
        }
        return false;
    }

    private function linhaDoToken(array $tokens, int $i): int
    {
        for ($j = $i; $j >= 0; $j--) {
            if (is_array($tokens[$j])) {
                return $tokens[$j][2] + substr_count($tokens[$j][1], "\n");
            }
        }
        return 0;
    }
}

final class QualityEvaluator
{
    public function __construct(
        private string $targetPath = '.',
        private string $format = 'table',
        private ?string $commit = null,
    ) {
        $this->targetPath = rtrim($targetPath, '/');
    }

    /** Percentil de posto mais próximo (nearest rank): x_(ceil(p*n)), sem interpolação. */
    public static function percentilPostoMaisProximo(array $valores, float $p): array
    {
        sort($valores);
        $n = count($valores);
        $r = (int) ceil($p * $n);
        return ['valor' => $valores[$r - 1], 'posto' => $r, 'n' => $n];
    }

    /** Nível S_i de uma métrica a partir das faixas do GQM (Tabela 4). */
    public static function nivel(string $metrica, float $valor): array
    {
        $faixas = [
            'M7a' => [[10, 4], [15, 3], [20, 2]],
            'M7b' => [[15, 4], [30, 3], [50, 2]],
        ];
        $nomes = [4 => 'Excelente', 3 => 'Bom', 2 => 'Regular', 1 => 'Crítico'];
        if ($metrica === 'M10') {
            $s = $valor >= 80 ? 4 : ($valor >= 60 ? 3 : ($valor >= 40 ? 2 : 1));
            return ['S' => $s, 'faixa' => $nomes[$s]];
        }
        foreach ($faixas[$metrica] as [$limite, $s]) {
            if ($valor <= $limite) {
                return ['S' => $s, 'faixa' => $nomes[$s]];
            }
        }
        return ['S' => 1, 'faixa' => $nomes[1]];
    }

    public function run(): array
    {
        $ausentes = array_values(array_filter(ARQUIVOS_ESCOPO, fn ($f) => !is_file($this->targetPath . '/' . $f)));
        $commit = $this->commit ?? $this->detectarCommit();

        $metricas = $this->pendentes();
        $inventario = [];
        $excluidos = [];

        if ($ausentes) {
            $status = 'nao_mensuravel';
            $nota = 'Arquivos do manifesto não encontrados em --path; M7a, M7b e M10 não são mensuráveis nesta execução.';
        } else {
            $analisador = new AnalisadorCallables();
            foreach (ARQUIVOS_ESCOPO as $arquivo) {
                $r = $analisador->analisarArquivo($this->targetPath . '/' . $arquivo, $arquivo);
                $inventario = array_merge($inventario, $r['callables']);
                $excluidos = array_merge($excluidos, $r['excluidos']);
            }
            [$metricas, $status, $nota] = $this->agregar($inventario, $metricas);
        }

        return [
            'instrumento' => [
                'nome' => 'scripts/evaluate-quality.php',
                'versao' => VERSAO_INSTRUMENTO,
                'php' => PHP_VERSION,
                'tokenizador' => 'token_get_all (TOKEN_PARSE)',
            ],
            'timestamp' => date('c'),
            'target_path' => $this->targetPath,
            'commit' => $commit,
            'status' => $status,
            'execution_note' => $nota,
            'manifesto' => ARQUIVOS_ESCOPO,
            'arquivos_ausentes' => $ausentes,
            'regras' => $this->regras(),
            'metrics' => $metricas,
            'inventario' => $inventario,
            'excluidos' => $excluidos,
            'summary' => [
                'total_files_audited' => $ausentes ? 0 : count(ARQUIVOS_ESCOPO),
                'total_callables' => count($inventario),
                'total_logical_lines' => array_sum(array_column($inventario, 'lloc')),
                'data_collection_status' => $status === 'executado'
                    ? 'M7a, M7b e M10 coletados; M8, M9 e M11 pendentes (Issue #44)'
                    : 'Não executado: manifesto ausente no diretório-alvo',
            ],
        ];
    }

    private function agregar(array $inventario, array $metricas): array
    {
        $n = count($inventario);
        if ($n === 0) {
            return [$metricas, 'nao_mensuravel', 'Nenhum callable concreto encontrado (n = 0).'];
        }
        $ccs = array_column($inventario, 'cc');
        $p90 = self::percentilPostoMaisProximo($ccs, 0.90);
        $max = max($ccs);
        $empatados = array_values(array_map(
            fn ($c) => $c['arquivo'] . ' :: ' . $c['simbolo'],
            array_filter($inventario, fn ($c) => $c['cc'] === $max)
        ));
        $semMi = array_values(array_filter($inventario, fn ($c) => $c['mi'] === null));
        $miMedio = $semMi ? null : array_sum(array_column($inventario, 'mi')) / $n;

        $metricas['M7a_CC_P90'] = array_merge($metricas['M7a_CC_P90'], [
            'value' => $p90['valor'], 'n' => $n, 'posto' => $p90['posto'],
            'status' => 'Coletado (Fase 4)',
        ] + self::nivel('M7a', $p90['valor']));
        $metricas['M7b_CC_MAX'] = array_merge($metricas['M7b_CC_MAX'], [
            'value' => $max, 'n' => $n, 'simbolos_no_maximo' => $empatados,
            'status' => 'Coletado (Fase 4)',
        ] + self::nivel('M7b', $max));
        $metricas['M10_MI'] = array_merge($metricas['M10_MI'], $miMedio === null
            ? ['value' => null, 'n' => $n, 'status' => 'Incompleto: ' . count($semMi) . ' callable(s) sem HV ou LOC válido']
            : ['value' => round($miMedio, 2), 'n' => $n, 'status' => 'Coletado (Fase 4)'] + self::nivel('M10', $miMedio));

        $metricas['M7a_CC_P90']['hipotese'] = ['id' => 'H3.1', 'criterio' => '10 < CC_P90 <= 20 e CC_max > 30',
            'resultado' => ($p90['valor'] > 10 && $p90['valor'] <= 20 && $max > 30) ? 'Confirmada' : 'Refutada'];
        if ($miMedio !== null) {
            $metricas['M10_MI']['hipotese'] = ['id' => 'H3.4', 'criterio' => '60 <= MI < 80',
                'resultado' => ($miMedio >= 60 && $miMedio < 80) ? 'Confirmada' : 'Refutada'];
        }

        return [$metricas, 'executado', 'M7a, M7b e M10 calculados sobre o manifesto congelado.'];
    }

    private function regras(): array
    {
        return [
            'unidade' => 'Callable concreto com corpo (método de classe, trait ou enum, ou função nomeada). Declarações abstratas e de interface são excluídas e listadas. Closures e funções anônimas são contadas dentro do callable que as contém.',
            'cc' => 'v(G) = 1 + pontos de decisão no corpo: if, elseif, for, foreach, while, case, braço de match (exceto default), catch, &&, ||, and, or, ?? e ternário (?). "else if" conta pelo if. "?" logo após "(", "," ou ":" é tipo anulável e não conta.',
            'halstead' => 'Operandos: variáveis, identificadores, nomes qualificados, literais numéricos e de texto e constantes mágicas. Operadores: os demais tokens significativos (palavras-chave, símbolos e pontuação); ")", "]" e "}" não contam, pois o par conta na abertura. Comentários, espaços e HTML embutido são ignorados. HV = N * log2(n).',
            'lloc' => 'LOC lógico = 1 (declaração) + ";" fora de parênteses no corpo + palavras-chave de estrutura (if, elseif, else, for, foreach, while, do, switch, case, default, try, catch, finally).',
            'mi' => 'MI_m = min(100, max(0, (171 - 5,2 ln(HV) - 0,23 v(G) - 16,2 ln(LOC)) / 171 * 100)); MI = média simples dos MI_m.',
            'p90' => 'Nearest rank: r = ceil(0,90 n), P90 = x_(r), sem interpolação.',
        ];
    }

    private function pendentes(): array
    {
        $pendente = fn (string $nome, string $simbolo, string $exc, string $crit, array $extra = []) => [
            'name' => $nome, 'symbol' => $simbolo, 'value' => null,
            'threshold_excellent' => $exc, 'threshold_critical' => $crit, 'status' => 'Pendente (Fase 4)',
        ] + $extra;

        return [
            'M7a_CC_P90' => $pendente('Complexidade Ciclomática P90', 'CC_P90', '<= 10', '> 20'),
            'M7b_CC_MAX' => $pendente('Complexidade Ciclomática Máxima', 'CC_max', '<= 15', '> 50'),
            'M8_DSPM' => $pendente('Distância da Sequência Principal de Martin', 'DSPM', '<= 0.20', '> 0.50', ['status' => 'Pendente (Issue #44)']),
            'M9_IFDL' => $pendente('Índice de Fricção de Dados Legado-Moderno', 'IFDL', '<= 1.0', '> 4.0', ['status' => 'Pendente (Issue #44)']),
            'M10_MI' => $pendente('Índice de Manutenibilidade Normalizado', 'MI', '>= 80', '< 40'),
            'M11_TTAE' => $pendente('Taxa de Testes Ativos com Asserção', 'TTAE', '>= 95.0%', '< 70.0%', ['unit' => '%', 'status' => 'Pendente (Issue #44)']),
        ];
    }

    private function detectarCommit(): ?string
    {
        if (!is_dir($this->targetPath . '/.git') || !function_exists('shell_exec')) {
            return null;
        }
        $sha = shell_exec('git -C ' . escapeshellarg($this->targetPath) . ' rev-parse HEAD 2>/dev/null');
        return $sha ? trim($sha) : null;
    }

    /** Grava as evidências separadas de M7 e M10 previstas no plano de medição. */
    public function gravarEvidencias(array $data, string $dir): void
    {
        if (!is_dir($dir) && !mkdir($dir, 0775, true)) {
            throw new RuntimeException("Não foi possível criar $dir");
        }
        $base = array_intersect_key($data, array_flip(['instrumento', 'timestamp', 'commit', 'status', 'manifesto', 'excluidos']));
        $m7 = $base + [
            'regras' => array_intersect_key($data['regras'], array_flip(['unidade', 'cc', 'p90'])),
            'M7a_CC_P90' => $data['metrics']['M7a_CC_P90'],
            'M7b_CC_MAX' => $data['metrics']['M7b_CC_MAX'],
            'inventario' => array_map(fn ($c) => array_intersect_key($c, array_flip(['arquivo', 'simbolo', 'linha_inicio', 'linha_fim', 'cc'])), $data['inventario']),
        ];
        $m10 = $base + [
            'regras' => array_intersect_key($data['regras'], array_flip(['unidade', 'cc', 'halstead', 'lloc', 'mi'])),
            'M10_MI' => $data['metrics']['M10_MI'],
            'inventario' => array_map(fn ($c) => array_intersect_key($c, array_flip(['arquivo', 'simbolo', 'linha_inicio', 'linha_fim', 'cc', 'halstead', 'hv', 'lloc', 'mi'])), $data['inventario']),
        ];
        $opcoes = JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE;
        file_put_contents("$dir/m7_complexidade.json", json_encode($m7, $opcoes) . PHP_EOL);
        file_put_contents("$dir/m10_mi.json", json_encode($m10, $opcoes) . PHP_EOL);
    }

    public function render(array $data): void
    {
        if ($this->format === 'json') {
            echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . PHP_EOL;
            return;
        }

        $linha = str_repeat('=', 80) . PHP_EOL;
        $traco = str_repeat('-', 80) . PHP_EOL;
        echo $linha;
        echo ' RELATÓRIO DO MOTOR DE AVALIAÇÃO ESTÁTICA — i-Educar (FGA0315 / ISO 25040)' . PHP_EOL;
        echo ' Instrumento próprio de medição v' . VERSAO_INSTRUMENTO . ' (Fase 4 — Execução da Avaliação)' . PHP_EOL;
        echo $linha;
        printf("Data/Hora:      %s\n", $data['timestamp']);
        printf("Diretório-alvo: %s\n", $data['target_path']);
        printf("Commit:         %s\n", $data['commit'] ?? 'não identificado');
        printf("Situação:       %s\n", $data['summary']['data_collection_status']);
        printf("Callables (n):  %d\n", $data['summary']['total_callables']);
        echo $traco;
        printf("%-10s %-40s %-10s %-20s\n", 'MÉTRICA', 'DESCRIÇÃO', 'VALOR', 'SITUAÇÃO');
        echo $traco;
        foreach ($data['metrics'] as $m) {
            $valor = $m['value'] === null ? 'null' : (string) $m['value'];
            $situacao = isset($m['faixa']) ? $m['faixa'] . ' (S=' . $m['S'] . ')' : $m['status'];
            printf("%-10s %-40s %-10s %-20s\n", $m['symbol'], mb_strimwidth($m['name'], 0, 40, '...'), $valor, $situacao);
        }
        echo $traco;

        if ($data['inventario']) {
            $ordenado = $data['inventario'];
            usort($ordenado, fn ($a, $b) => $b['cc'] <=> $a['cc']);
            echo 'Callables de maior complexidade:' . PHP_EOL;
            foreach (array_slice($ordenado, 0, 10) as $c) {
                printf("  v(G)=%-4d MI=%-7s %s :: %s (linha %d)\n", $c['cc'], $c['mi'] ?? 'null', basename($c['arquivo']), $c['simbolo'], $c['linha_inicio']);
            }
            echo $traco;
        }
        echo $data['execution_note'] . PHP_EOL;
        echo $linha;
    }
}

// Execução CLI
if (PHP_SAPI === 'cli' && realpath($argv[0] ?? '') === __FILE__) {
    $format = 'table';
    $path = '.';
    $commit = null;
    $evidencias = null;

    foreach (array_slice($argv, 1) as $arg) {
        if ($arg === '--json' || $arg === '--format=json') {
            $format = 'json';
        } elseif (str_starts_with($arg, '--path=')) {
            $path = substr($arg, 7);
        } elseif (str_starts_with($arg, '--commit=')) {
            $commit = substr($arg, 9);
        } elseif (str_starts_with($arg, '--evidence-dir=')) {
            $evidencias = substr($arg, 15);
        }
    }

    $evaluator = new QualityEvaluator($path, $format, $commit);
    $data = $evaluator->run();
    if ($evidencias !== null && $data['status'] === 'executado') {
        $evaluator->gravarEvidencias($data, $evidencias);
    }
    $evaluator->render($data);
    exit(0);
}
