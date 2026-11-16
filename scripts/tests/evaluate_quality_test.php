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

// Testes de limiares M8, M9 e M11
verificar('faixa M8 0.15 é Excelente', QualityEvaluator::nivel('M8', 0.15)['S'], 4);
verificar('faixa M8 0.42 é Regular', QualityEvaluator::nivel('M8', 0.42)['S'], 2);
verificar('faixa M8 0.55 é Crítico', QualityEvaluator::nivel('M8', 0.55)['S'], 1);
verificar('faixa M9 0.8 é Excelente', QualityEvaluator::nivel('M9', 0.8)['S'], 4);
verificar('faixa M9 2.0 é Bom', QualityEvaluator::nivel('M9', 2.0)['S'], 3);
verificar('faixa M9 4.5 é Crítico', QualityEvaluator::nivel('M9', 4.5)['S'], 1);
verificar('faixa M11 96% é Excelente', QualityEvaluator::nivel('M11', 96.0)['S'], 4);
verificar('faixa M11 75% é Regular', QualityEvaluator::nivel('M11', 75.0)['S'], 2);
verificar('faixa M11 65% é Crítico', QualityEvaluator::nivel('M11', 65.0)['S'], 1);

// Teste de AnalisadorFriccaoLegadoM9 em modelo sintético
$modeloCodigo = <<<'PHP'
<?php
namespace App\Models;
class DummyModel {
    protected $table = 'pmieducar.dummy';
    protected $primaryKey = 'cod_dummy';
    public const CREATED_AT = 'data_cad';
    public array $legacy = ['id' => 'cod_dummy'];
    protected $casts = ['data' => 'date', 'ativo' => 'bool'];
    protected function name(): Attribute {
        return Attribute::make(get: fn() => 'test');
    }
}
PHP;
$dirDummy = sys_get_temp_dir() . '/m9_test_' . uniqid();
mkdir($dirDummy . '/app/Models', 0777, true);
file_put_contents($dirDummy . '/app/Models/DummyModel.php', $modeloCodigo);
$m9Res = (new AnalisadorFriccaoLegadoM9())->analisar($dirDummy, [
    'modelos' => [
        ['classe' => 'DummyModel', 'caminho' => 'app/Models/DummyModel.php', 'tabela' => 'pmieducar.dummy']
    ]
]);
unlink($dirDummy . '/app/Models/DummyModel.php');
rmdir($dirDummy . '/app/Models');
rmdir($dirDummy . '/app');
rmdir($dirDummy);

// 1 table + 1 primaryKey + 1 const + 1 legacy + 1 casts + 1 attribute = 6 adaptadores
verificar('M9 adaptadores detectados no DummyModel', $m9Res['total_adaptadores'], 6);
verificar('M9 ifdl calculado no DummyModel', $m9Res['ifdl'], 6.0);

// Teste de AnalisadorTestesM11 via JUnit XML real do runner (sem regressão para regex estática)
$dirTestDummy = sys_get_temp_dir() . '/m11_test_' . uniqid();
mkdir($dirTestDummy . '/tests', 0777, true);
$m11SemJunit = (new AnalisadorTestesM11())->analisar($dirTestDummy, [
    'arquivos_teste' => ['tests/DummyTest.php']
]);
verificar('M11 sem JUnit retorna nao_mensuravel', $m11SemJunit['status'], 'nao_mensuravel');
verificar('M11 sem JUnit retorna ttae null', $m11SemJunit['ttae'], null);

$junitXmlDummy = <<<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="Tests\DummyTest" file="tests/DummyTest.php" tests="6" assertions="11" errors="0" failures="1" skipped="2">
    <testcase name="caso um ativo" file="tests/DummyTest.php::caso um ativo" class="Tests\DummyTest" assertions="3" time="0.01"/>
    <testcase name="caso dois skipped" file="tests/DummyTest.php::caso dois skipped" class="Tests\DummyTest" assertions="0" time="0.01"><skipped/></testcase>
    <testcase name="caso tres skip apos assercao" file="tests/DummyTest.php::caso tres skip apos assercao" class="Tests\DummyTest" assertions="5" time="0.01"><skipped/></testcase>
    <testcase name="caso quatro vazio" file="tests/DummyTest.php::caso quatro vazio" class="Tests\DummyTest" assertions="0" time="0.01"/>
    <testcase name="caso cinco falha" file="tests/DummyTest.php::caso cinco falha" class="Tests\DummyTest" assertions="1" time="0.01"><failure>fail</failure></testcase>
    <testcase name="caso seis outro ativo" file="tests/DummyTest.php::caso seis outro ativo" class="Tests\DummyTest" assertions="2" time="0.01"/>
  </testsuite>
</testsuites>
XML;
$junitDummyPath = $dirTestDummy . '/junit.xml';
file_put_contents($junitDummyPath, $junitXmlDummy);
$m11Res = (new AnalisadorTestesM11())->analisar($dirTestDummy, [
    'arquivos_teste' => ['tests/DummyTest.php']
], $junitDummyPath);
unlink($junitDummyPath);
rmdir($dirTestDummy . '/tests');
rmdir($dirTestDummy);

verificar('M11 total descobertos no DummyTest', $m11Res['total_declarados'], 6);
verificar('M11 total skips no DummyTest', $m11Res['total_skips'], 2);
verificar('M11 ativos sem asserção (teste vazio) excluídos no DummyTest', $m11Res['ativos_sem_assercao'], 1);
verificar('M11 total falhas no DummyTest', $m11Res['total_falhas'], 1);
verificar('M11 ativos com asserção no DummyTest', $m11Res['ativos_com_assercao'], 2);
verificar('M11 ttae no DummyTest exclui skipped, vazios e falhas', $m11Res['ttae'], 33.33);

// Teste de AnalisadorComponentesM8: duas classes consumidoras da mesma classe + aliases/namespaces
$dirM8 = sys_get_temp_dir() . '/m8_test_' . uniqid();
mkdir($dirM8 . '/app/Consumers', 0777, true);
mkdir($dirM8 . '/app/Domain', 0777, true);
mkdir($dirM8 . '/legacy', 0777, true);

file_put_contents($dirM8 . '/app/Domain/Target.php', <<<'PHP'
<?php
namespace App\Domain;
class Target {}
PHP);
file_put_contents($dirM8 . '/app/Consumers/ConsumerOne.php', <<<'PHP'
<?php
namespace App\Consumers;
use App\Domain\Target as AliasedTarget;
class ConsumerOne {
    public function run(AliasedTarget $t): void {}
}
PHP);
file_put_contents($dirM8 . '/app/Consumers/ConsumerTwo.php', <<<'PHP'
<?php
namespace App\Consumers;
use App\Domain;
class ConsumerTwo {
    public function run(): Domain\Target {
        return new \App\Domain\Target();
    }
}
PHP);
// Classe com mesmo nome curto em namespace distinto não deve colidir
file_put_contents($dirM8 . '/app/Consumers/SharedController.php', <<<'PHP'
<?php
namespace App\Consumers;
class SharedController {}
PHP);
file_put_contents($dirM8 . '/legacy/SharedController.php', <<<'PHP'
<?php
class SharedController {}
PHP);

$m8Res = (new AnalisadorComponentesM8())->analisar($dirM8, [
    'componentes' => [
        'CompA' => [
            'nome' => 'Consumidores',
            'arquivos' => [
                'app/Consumers/ConsumerOne.php',
                'app/Consumers/ConsumerTwo.php',
                'app/Consumers/SharedController.php',
            ],
        ],
        'CompB' => [
            'nome' => 'Alvo',
            'arquivos' => [
                'app/Domain/Target.php',
                'legacy/SharedController.php',
            ],
        ],
    ],
]);

foreach (['/app/Consumers/ConsumerOne.php', '/app/Consumers/ConsumerTwo.php', '/app/Consumers/SharedController.php', '/app/Domain/Target.php', '/legacy/SharedController.php'] as $f) {
    unlink($dirM8 . $f);
}
rmdir($dirM8 . '/app/Consumers');
rmdir($dirM8 . '/app/Domain');
rmdir($dirM8 . '/app');
rmdir($dirM8 . '/legacy');
rmdir($dirM8);

verificar('M8 duas consumidoras geram Ca=2 no componente alvo', $m8Res['componentes']['CompB']['ca'], 2);
verificar('M8 componente consumidor consome 1 tipo externo (Ce=1)', $m8Res['componentes']['CompA']['ce'], 1);
verificar('M8 total de pares distintos preservando classe de origem', $m8Res['total_pares_dependencia'], 2);
verificar('M8 sem colisão entre SharedController namespaced e global', $m8Res['componentes']['CompA']['ca'], 0);
verificar('M8 DSPM com pares distintos', $m8Res['dspm'], 0.5);

echo $falhas === 0 ? 'Todos os testes passaram.' . PHP_EOL : "$falhas teste(s) falharam." . PHP_EOL;
exit($falhas === 0 ? 0 : 1);
