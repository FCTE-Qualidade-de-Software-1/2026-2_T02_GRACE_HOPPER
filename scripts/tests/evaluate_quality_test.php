<?php
/**
 * Testes do motor de avaliação estática (scripts/evaluate-quality.php).
 * Execução: php scripts/tests/evaluate_quality_test.php
 */

declare(strict_types=1);

require __DIR__ . '/../evaluate-quality.php';

$falhas = 0;
function verificar(string $nome, mixed $obtido, mixed $esperado): void
{
    global $falhas;
    if ($obtido === $esperado) {
        echo "ok   $nome" . PHP_EOL;
        return;
    }
    $falhas++;
    echo "FALHA $nome: esperado " . var_export($esperado, true) . ', obtido ' . var_export($obtido, true) . PHP_EOL;
}

$codigo = <<<'PHP'
<?php
interface Contrato
{
    public function assinatura(?int $x): ?string;
}

abstract class Base
{
    abstract protected function abstrato(): void;
}

class Exemplo extends Base implements Contrato
{
    public function assinatura(?int $x): ?string
    {
        return $x?->valor ?? null;
    }

    protected function abstrato(): void
    {
    }

    public function decisoes(array $itens, bool $a, bool $b): int
    {
        $total = 0;
        foreach ($itens as $item) {
            if ($a && $b) {
                $total++;
            } elseif ($a || $b) {
                $total += $item > 0 ? 1 : 2;
            } else if ($item) {
                $total--;
            }
        }
        for ($i = 0; $i < 3; $i++) {
            $total += $i;
        }
        switch ($total) {
            case 1:
                return 1;
            case 2:
                return 2;
            default:
                break;
        }
        try {
            $f = function (?int $v) {
                return $v ? 1 : 0;
            };
        } catch (Exception $e) {
            return -1;
        }
        return $total;
    }
}

function comMatch(int $x): int
{
    return match (true) {
        $x > 1 && $x < 5 => 1,
        $x === 0 => ['a' => 1, 'b' => 2][0] ?? 0,
        default => 3,
    };
}

function solta(): void
{
    $c = new class {
        public function interno(): int
        {
            return 1;
        }
    };
}
PHP;

$arquivo = tempnam(sys_get_temp_dir(), 'eq');
file_put_contents($arquivo, $codigo);
$r = (new AnalisadorCallables())->analisarArquivo($arquivo, 'exemplo.php');
unlink($arquivo);

$porSimbolo = [];
foreach ($r['callables'] as $c) {
    $porSimbolo[$c['simbolo']] = $c;
}

verificar('callables concretos', array_keys($porSimbolo), ['Exemplo::assinatura', 'Exemplo::abstrato', 'Exemplo::decisoes', 'comMatch', 'solta']);
verificar('declarações sem corpo excluídas', array_column($r['excluidos'], 'simbolo'), ['Contrato::assinatura', 'Base::abstrato']);
// ?? conta; ?int, ?string e ?-> não contam.
verificar('v(G) com tipos anuláveis e coalescência', $porSimbolo['Exemplo::assinatura']['cc'], 2);
verificar('v(G) de método vazio', $porSimbolo['Exemplo::abstrato']['cc'], 1);
// 1 + foreach + if + && + elseif + || + ternário + if (else if) + for + 2 case + ternário da closure + catch = 13
verificar('v(G) com laços, switch, closure e catch', $porSimbolo['Exemplo::decisoes']['cc'], 13);
// 1 + 2 braços do match (default não conta) + && + ?? = 5; "=>" do array interno não conta.
verificar('v(G) com match', $porSimbolo['comMatch']['cc'], 5);
verificar('método de classe anônima fica no callable externo', $porSimbolo['solta']['cc'], 1);
verificar('LOC lógico de método vazio', $porSimbolo['Exemplo::abstrato']['lloc'], 1);
verificar('MI dentro de [0, 100]', $porSimbolo['Exemplo::decisoes']['mi'] >= 0 && $porSimbolo['Exemplo::decisoes']['mi'] <= 100, true);

$p = QualityEvaluator::percentilPostoMaisProximo([5, 1, 9, 3, 7, 2, 8, 4, 6, 10, 11], 0.90);
verificar('P90 por nearest rank (n = 11, r = 10)', [$p['valor'], $p['posto']], [10, 10]);
verificar('faixa M7a 10 é Excelente', QualityEvaluator::nivel('M7a', 10)['S'], 4);
verificar('faixa M7a 20 é Regular', QualityEvaluator::nivel('M7a', 20)['S'], 2);
verificar('faixa M7b 51 é Crítico', QualityEvaluator::nivel('M7b', 51)['S'], 1);
verificar('faixa M10 60 é Bom', QualityEvaluator::nivel('M10', 60.0)['S'], 3);

$sem = (new QualityEvaluator('/caminho/inexistente'))->run();
verificar('sem manifesto não há valor arbitrado', [$sem['status'], $sem['metrics']['M7a_CC_P90']['value']], ['nao_mensuravel', null]);

echo $falhas === 0 ? 'Todos os testes passaram.' . PHP_EOL : "$falhas teste(s) falharam." . PHP_EOL;
exit($falhas === 0 ? 0 : 1);
