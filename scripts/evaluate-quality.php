#!/usr/bin/env php
<?php
/**
 * Motor de Avaliação Estática de Qualidade de Software — i-Educar 2.12
 * Disciplina: Qualidade de Software 1 (FGA0315) - UnB / FGA
 * Framework GQM: M7a (CC P90), M7b (CC Max), M8 (DSPM), M9 (IFDL), M10 (MI) e M11 (TTAE)
 * Issue #11: Planejamento das Ferramentas de Análise Estática e Motor PHP
 *
 * NOTA METODOLÓGICA (Fase 3 — ISO/IEC 25040:2024):
 * Este script constitui o instrumento planejado e estruturado pela equipe para a extração
 * de métricas estáticas de manutenibilidade. A execução e a coleta de dados brutos sobre
 * o checkout oficial do repositório 'portabilis/i-educar' ocorrerão na Fase 4 (Execução da Avaliação).
 * Portanto, este instrumento não retorna valores fictícios ou previamente arbitrados.
 */

declare(strict_types=1);

class QualityEvaluator
{
    private string $targetPath;
    private string $format;

    public function __construct(string $targetPath = '.', string $format = 'table')
    {
        $this->targetPath = rtrim($targetPath, '/');
        $this->format = $format;
    }

    /**
     * Calcula a complexidade ciclomática de um código PHP via análise de tokens (token_get_all).
     * Instrumento preparado para a Fase 4.
     */
    public function calculateCyclomaticComplexity(string $code): int
    {
        $tokens = token_get_all($code);
        $complexity = 1;

        $decisionTokens = [
            T_IF, T_ELSEIF, T_FOR, T_FOREACH, T_WHILE, T_CASE, T_CATCH,
            T_BOOLEAN_AND, T_BOOLEAN_OR, T_COALESCE
        ];

        foreach ($tokens as $token) {
            if (is_array($token) && in_array($token[0], $decisionTokens, true)) {
                $complexity++;
            } elseif ($token === '?') {
                $complexity++;
            }
        }

        return $complexity;
    }

    /**
     * Retorna a estrutura das métricas planejadas.
     * Na Fase 3 (Planejamento), os valores são nulos até a execução dos testes no checkout da aplicação.
     */
    public function run(): array
    {
        return [
            'timestamp' => date('c'),
            'target_path' => $this->targetPath,
            'status' => 'planejado_fase_3',
            'execution_note' => 'Cálculo e extração pendentes de execução no checkout versionado do i-Educar (Fase 4 - Execução da Avaliação)',
            'metrics' => [
                'M7a_CC_P90' => [
                    'name' => 'Complexidade Ciclomática P90',
                    'symbol' => 'CC_P90',
                    'value' => null,
                    'threshold_excellent' => '<= 10',
                    'threshold_critical' => '> 20',
                    'status' => 'Pendente (Fase 4)'
                ],
                'M7b_CC_MAX' => [
                    'name' => 'Complexidade Ciclomática Máxima',
                    'symbol' => 'CC_max',
                    'value' => null,
                    'threshold_excellent' => '<= 15',
                    'threshold_critical' => '> 50',
                    'status' => 'Pendente (Fase 4)'
                ],
                'M8_DSPM' => [
                    'name' => 'Distância da Sequência Principal de Martin',
                    'symbol' => 'DSPM',
                    'value' => null,
                    'threshold_excellent' => '<= 0.20',
                    'threshold_critical' => '> 0.50',
                    'status' => 'Pendente (Fase 4)'
                ],
                'M9_IFDL' => [
                    'name' => 'Índice de Fricção de Dados Legado-Moderno',
                    'symbol' => 'IFDL',
                    'value' => null,
                    'threshold_excellent' => '<= 1.0',
                    'threshold_critical' => '> 4.0',
                    'status' => 'Pendente (Fase 4)'
                ],
                'M10_MI' => [
                    'name' => 'Índice de Manutenibilidade Normalizado',
                    'symbol' => 'MI',
                    'value' => null,
                    'threshold_excellent' => '>= 80',
                    'threshold_critical' => '< 40',
                    'status' => 'Pendente (Fase 4)'
                ],
                'M11_TTAE' => [
                    'name' => 'Taxa de Testes Ativos com Asserção',
                    'symbol' => 'TTAE',
                    'value' => null,
                    'unit' => '%',
                    'threshold_excellent' => '>= 95.0%',
                    'threshold_critical' => '< 70.0%',
                    'status' => 'Pendente (Fase 4)'
                ]
            ],
            'summary' => [
                'total_files_audited' => 0,
                'total_lines_of_code' => 0,
                'total_test_cases' => 0,
                'skipped_tests_detected' => 0,
                'data_collection_status' => 'Não executado (Instrumento em fase de projeto — ISO/IEC 25040:2024)'
            ]
        ];
    }

    public function render(array $data): void
    {
        if ($this->format === 'json') {
            echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . PHP_EOL;
            return;
        }

        echo "================================================================================" . PHP_EOL;
        echo " RELATÓRIO DO MOTOR DE AVALIAÇÃO ESTÁTICA — i-Educar (FGA0315 / ISO 25040)" . PHP_EOL;
        echo " Instrumento Próprio de Medição (Fase 3 — Projeto da Avaliação)" . PHP_EOL;
        echo "================================================================================" . PHP_EOL;
        echo sprintf("Data/Hora:     %s" . PHP_EOL, $data['timestamp']);
        echo sprintf("Diretório-alvo:%s" . PHP_EOL, $data['target_path']);
        echo sprintf("Status:        %s" . PHP_EOL, $data['summary']['data_collection_status']);
        echo "Aviso:         Nenhum dado é arbitrado antes da execução no checkout do produto." . PHP_EOL;
        echo "--------------------------------------------------------------------------------" . PHP_EOL;
        printf("%-10s %-40s %-12s %-16s\n", "MÉTRICA", "DESCRIÇÃO", "VALOR", "SITUAÇÃO");
        echo "--------------------------------------------------------------------------------" . PHP_EOL;

        foreach ($data['metrics'] as $key => $metric) {
            $valStr = $metric['value'] === null ? 'null' : (string)$metric['value'];
            printf("%-10s %-40s %-12s %-16s\n", 
                $metric['symbol'], 
                mb_strimwidth($metric['name'], 0, 40, '...'), 
                $valStr, 
                $metric['status']
            );
        }

        echo "--------------------------------------------------------------------------------" . PHP_EOL;
        echo "Estágio: INSTRUMENTO PLANEJADO (Execução prevista para a Fase 4 / Release E2)" . PHP_EOL;
        echo "================================================================================" . PHP_EOL;
    }
}

// Execução CLI
$format = 'table';
$path = '.';

foreach ($argv as $arg) {
    if ($arg === '--json' || $arg === '--format=json') {
        $format = 'json';
    } elseif (str_starts_with($arg, '--path=')) {
        $path = substr($arg, 7);
    }
}

$evaluator = new QualityEvaluator($path, $format);
$data = $evaluator->run();
$evaluator->render($data);
exit(0);
