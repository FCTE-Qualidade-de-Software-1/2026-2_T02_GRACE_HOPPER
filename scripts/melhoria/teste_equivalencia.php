<?php

declare(strict_types=1);

/**
 * Teste de equivalência da ação de melhoria em Avaliacao_Service_Boletim::getSituacaoNotas.
 *
 * Extrai getSituacaoNotas (e os métodos auxiliares novos) da versão original e da versão
 * refatorada de Boletim.php, executa as duas sobre os mesmos cenários gerados de forma
 * pseudoaleatória e compara o resultado (situação geral e situação por componente) ou a
 * exceção lançada. As dependências de banco e de configuração são substituídas por dublês
 * que devolvem os valores do cenário.
 *
 * Uso:
 *   php scripts/melhoria/teste_equivalencia.php \
 *       --original=/caminho/i-educar/ieducar/modules/Avaliacao/Service/Boletim.php \
 *       --refatorado=docs/evidencias/melhoria/Boletim.refatorado.php \
 *       [--casos=20000] [--semente=2026] [--autoteste]
 *
 * Com --autoteste, o script também injeta um defeito na versão refatorada e confirma que o
 * teste detecta divergências (prova de que o oráculo não é trivial).
 */

final class App_Model_MatriculaSituacao
{
    const APROVADO = 1;
    const REPROVADO = 2;
    const EM_ANDAMENTO = 3;
    const EM_EXAME = 7;
    const APROVADO_APOS_EXAME = 8;
}

final class RegraAvaliacao_Model_Nota_TipoValor
{
    const NENHUM = 0;
    const NUMERICA = 1;
    const CONCEITUAL = 2;
    const NUMERICACONCEITUAL = 3;
}

final class RegraAvaliacao_Model_TipoProgressao
{
    const CONTINUADA = 1;
    const NAO_CONTINUADA_MEDIA_PRESENCA = 2;
    const NAO_CONTINUADA_SOMENTE_MEDIA = 3;
    const NAO_CONTINUADA_MANUAL = 4;
    const NAO_CONTINUADA_MANUAL_CICLO = 5;
}

final class App_Model_IedFinder
{
    public static array $caso = [];

    public static function getComponentesPorMatricula(...$args)
    {
        return self::$caso['componentesMatricula'];
    }

    public static function verificaSeExisteNotasComponenteCurricular($matriculaId, $componenteId)
    {
        return [['cc' => self::$caso['existeNota'][$componenteId] ?? 0]];
    }
}

final class clsPmieducarTurma
{
    public static array $caso = [];

    public static function getDisciplinaDispensada($turmaId)
    {
        return self::$caso['disciplinaDispensada'];
    }
}

/** Dublê da classe Avaliacao_Service_Boletim: cada dependência devolve o valor do cenário. */
abstract class BoletimFalso
{
    protected $_situacaoPrioridade = [
        App_Model_MatriculaSituacao::EM_ANDAMENTO => 1,
        App_Model_MatriculaSituacao::EM_EXAME => 2,
        App_Model_MatriculaSituacao::REPROVADO => 3,
        App_Model_MatriculaSituacao::APROVADO_APOS_EXAME => 4,
        App_Model_MatriculaSituacao::APROVADO => 5,
    ];

    public function __construct(protected array $c)
    {
    }

    public function getOption($nome)
    {
        return match ($nome) {
            'matriculaData' => ['cod_matricula' => 501],
            'etapaAtual' => null,
            'ref_cod_turma' => 201,
            'etapas' => $this->c['etapas'],
        };
    }

    public function _loadMedias() { return $this; }
    public function getMediasComponentes() { return $this->c['medias']; }
    public function getComponentes() { return $this->c['componentes']; }
    public function codigoDisciplinasAglutinadas() { return $this->c['aglutinados']; }
    public function getRegraAvaliacaoTipoNota() { return $this->c['tipoNota']; }
    public function getRegraAvaliacaoNotaGeralPorEtapa() { return $this->c['notaGeralPorEtapa']; }
    public function getMediaGeral() { return $this->c['mediaGeral']; }
    public function getRegraAvaliacaoMedia() { return $this->c['media']; }
    public function hasRegraAvaliacaoFormulaRecuperacao() { return $this->c['formulaRecuperacao']; }
    public function getRegraAvaliacaoMediaRecuperacao() { return $this->c['mediaRecuperacao']; }
    public function getRegraAvaliacaoAprovarPelaFrequenciaAposExame() { return $this->c['aprovarFrequencia']; }
    public function getQtdComponentes($ignorar = false, $naoReprovativas = []) { return $this->c['qtdComponentes']; }
    public function getRegraAvaliacaoDefinirComponentePorEtapa() { return $this->c['componentePorEtapa']; }
    public function getLastStage($matricula, $turma, $id) { return $this->c['ultimaEtapa'][$id]; }
    public function getRegraAvaliacaoTipoProgressao() { return $this->c['tipoProgressao']; }
    public function hasRegraAvaliacaoReprovacaoAutomatica() { return $this->c['reprovacaoAutomatica']; }
    public function preverNotaRecuperacao($id) { return $this->c['previsao'][$id]; }
    public function getRegraAvaliacaoNotaMaximaExameFinal() { return $this->c['notaMaximaExame']; }
    public function hasRegraAvaliacaoAprovaMediaDisciplina() { return $this->c['aprovaMediaDisciplina']; }
    public function hasReprovarAutomaticamenteAposDependencias() { return $this->c['reprovarAposDependencias']; }
    public function getQtdeReprovarAutomaticamenteAposDependencias() { return $this->c['qtdeReprovar']; }

    // Cópias fiéis dos métodos auxiliares de leitura usados por getSituacaoNotas.
    public function exibeSituacao($componenteCurricularId): bool
    {
        $codigos = $this->codigoDisciplinasAglutinadas();

        return empty($codigos) || !in_array($componenteCurricularId, $codigos) || $componenteCurricularId == $codigos[0];
    }

    public function valorMediaSituacao($mediaComponente)
    {
        $numerica = $this->getRegraAvaliacaoTipoNota() == RegraAvaliacao_Model_Nota_TipoValor::NUMERICA;

        return (float) ($numerica ? $mediaComponente->mediaArredondada : $mediaComponente->media);
    }
}

/** Extrai o código-fonte dos métodos de uma classe PHP, pelo nome, usando o tokenizador. */
function extrairMetodos(string $codigo): array
{
    $tokens = token_get_all($codigo);
    $metodos = [];
    $n = count($tokens);
    for ($i = 0; $i < $n; $i++) {
        if (!is_array($tokens[$i]) || $tokens[$i][0] !== T_FUNCTION) {
            continue;
        }
        $j = $i + 1;
        while ($j < $n && is_array($tokens[$j]) && $tokens[$j][0] === T_WHITESPACE) {
            $j++;
        }
        if (!is_array($tokens[$j]) || $tokens[$j][0] !== T_STRING) {
            continue; // closure
        }
        $nome = $tokens[$j][1];
        // início: modificadores antes de "function"
        $inicio = $i;
        for ($k = $i - 1; $k >= 0; $k--) {
            $t = $tokens[$k];
            if (is_array($t) && in_array($t[0], [T_WHITESPACE, T_PUBLIC, T_PROTECTED, T_PRIVATE, T_STATIC, T_FINAL, T_ABSTRACT], true)) {
                if ($t[0] !== T_WHITESPACE) {
                    $inicio = $k;
                }
                continue;
            }
            break;
        }
        // fim: chave que fecha o corpo
        $k = $j;
        while ($k < $n && $tokens[$k] !== '{' && $tokens[$k] !== ';') {
            $k++;
        }
        if ($tokens[$k] === ';') {
            continue;
        }
        $nivel = 0;
        for (; $k < $n; $k++) {
            $t = $tokens[$k];
            if ($t === '{' || (is_array($t) && in_array($t[0], [T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES], true))) {
                $nivel++;
            } elseif ($t === '}') {
                $nivel--;
                if ($nivel === 0) {
                    break;
                }
            }
        }
        $texto = '';
        for ($m = $inicio; $m <= $k; $m++) {
            $texto .= is_array($tokens[$m]) ? $tokens[$m][1] : $tokens[$m];
        }
        $metodos[$nome] = $texto;
    }

    return $metodos;
}

function montarClasse(string $nomeClasse, array $metodosArquivo, array $metodosOriginais): void
{
    $incluir = ['getSituacaoNotas', '_situacaoPrioritaria'];
    foreach (array_keys($metodosArquivo) as $nome) {
        if (!isset($metodosOriginais[$nome])) {
            $incluir[] = $nome; // método auxiliar criado pela refatoração
        }
    }
    $corpo = '';
    foreach (array_unique($incluir) as $nome) {
        if (!isset($metodosArquivo[$nome])) {
            throw new RuntimeException("Método $nome não encontrado.");
        }
        $corpo .= "\n    " . $metodosArquivo[$nome] . "\n";
    }
    eval("final class $nomeClasse extends BoletimFalso {" . $corpo . '}');
}

function gerarCaso(): array
{
    $ids = [11, 12, 13, 14, 15, 16];
    $escolher = fn (array $lista) => $lista[array_rand($lista)];
    $subconjunto = function (array $lista, int $min = 0) {
        $s = array_values(array_filter($lista, fn () => mt_rand(0, 1) === 1));

        return count($s) >= $min ? $s : array_slice($lista, 0, $min);
    };
    $nota = fn () => round(mt_rand(0, 100) / 10, 1);

    $componentesMatricula = [];
    foreach ($subconjunto($ids) as $id) {
        $componentesMatricula[$id] = (object) ['id' => $id, 'desconsidera_para_progressao' => mt_rand(0, 4) === 0];
    }
    $medias = [];
    foreach ($subconjunto($ids) as $id) {
        $m = $nota();
        $medias[$id] = [(object) [
            'etapa' => $escolher([1, 2, 3, 4, '1', '2', '3', '4', 'Rc']),
            'situacao' => $escolher([1, 2, 3, 7, 8]),
            'media' => $m,
            'mediaArredondada' => round($m),
        ]];
    }
    $componentes = [];
    foreach ($subconjunto($ids) as $id) {
        $componentes[$id] = (object) ['id' => $id];
    }
    // Disciplinas aglutinadas são componentes da matrícula que têm média lançada.
    $aglutinados = [];
    if ($medias && mt_rand(0, 3) === 0) {
        $aglutinados = $subconjunto(array_keys($medias), 1);
        foreach ($aglutinados as $id) {
            $componentesMatricula[$id] ??= (object) ['id' => $id, 'desconsidera_para_progressao' => false];
            $componentes[$id] ??= (object) ['id' => $id];
        }
    }
    $ultimaEtapa = $existeNota = $previsao = [];
    foreach ($ids as $id) {
        $ultimaEtapa[$id] = $escolher([1, 2, 3, 4, '4']);
        $existeNota[$id] = mt_rand(0, 1);
        $previsao[$id] = $escolher([null, '+10', '+8', 5.5, '7', '+10.0']);
    }
    $mg = $nota();

    return [
        'calcularSituacaoAluno' => (bool) mt_rand(0, 1),
        'componentesMatricula' => $componentesMatricula,
        'medias' => $medias,
        'componentes' => $componentes,
        'aglutinados' => $aglutinados,
        'disciplinaDispensada' => mt_rand(0, 3) === 0 ? $escolher($ids) : null,
        'tipoNota' => $escolher([0, 1, 1, 2, 3]),
        'notaGeralPorEtapa' => $escolher(['0', '0', '0', '1', null]),
        'mediaGeral' => (object) ['media' => $mg, 'mediaArredondada' => round($mg), 'etapa' => $escolher([1, 2, 3, 4, 'Rc'])],
        'etapas' => $escolher([1, 2, 3, 4]),
        'media' => $escolher([5, 6, 7, 6.0]),
        'mediaRecuperacao' => $escolher([5, 6, 7]),
        'formulaRecuperacao' => (bool) mt_rand(0, 1),
        'aprovarFrequencia' => (bool) mt_rand(0, 1),
        'qtdComponentes' => mt_rand(0, 7),
        'componentePorEtapa' => $escolher(['0', '1', null]),
        'ultimaEtapa' => $ultimaEtapa,
        'tipoProgressao' => $escolher([1, 2, 3, 3, 4, 5]),
        'existeNota' => $existeNota,
        'reprovacaoAutomatica' => (bool) mt_rand(0, 1),
        'previsao' => $previsao,
        'notaMaximaExame' => $escolher([10, 8, '10']),
        'aprovaMediaDisciplina' => (bool) mt_rand(0, 1),
        'reprovarAposDependencias' => mt_rand(0, 2) === 0,
        'qtdeReprovar' => mt_rand(0, 3),
    ];
}

function executar(string $classe, array $caso): string
{
    App_Model_IedFinder::$caso = $caso;
    clsPmieducarTurma::$caso = $caso;
    try {
        $r = (new $classe($caso))->getSituacaoNotas($caso['calcularSituacaoAluno']);

        return 'ok:' . json_encode($r, JSON_PRESERVE_ZERO_FRACTION);
    } catch (Throwable $e) {
        return 'erro:' . get_class($e) . ':' . $e->getMessage();
    }
}

function comparar(string $a, string $b, int $casos, int $semente): array
{
    mt_srand($semente);
    $divergencias = [];
    $resultados = [];
    for ($i = 0; $i < $casos; $i++) {
        $caso = gerarCaso();
        $ra = executar($a, $caso);
        $rb = executar($b, $caso);
        if ($ra !== $rb) {
            $divergencias[] = ['caso' => $i, 'original' => $ra, 'refatorado' => $rb];
        }
        $chave = str_starts_with($ra, "erro:") ? "exceção (" . substr($ra, 5, 90) . ")" : 'situação ' . json_decode(substr($ra, 3))->situacao;
        $resultados[$chave] = ($resultados[$chave] ?? 0) + 1;
    }
    ksort($resultados);

    return [$divergencias, $resultados];
}

$opcoes = getopt('', ['original:', 'refatorado:', 'casos::', 'semente::', 'autoteste']);
if (empty($opcoes['original']) || empty($opcoes['refatorado'])) {
    fwrite(STDERR, "Uso: php teste_equivalencia.php --original=Boletim.php --refatorado=Boletim.refatorado.php [--casos=N] [--semente=S] [--autoteste]\n");
    exit(2);
}
$casos = (int) ($opcoes['casos'] ?? 20000);
$semente = (int) ($opcoes['semente'] ?? 2026);

set_error_handler(function (int $nivel, string $mensagem) {
    throw new ErrorException($mensagem, 0, $nivel);
});

$fonteOriginal = (string) file_get_contents($opcoes['original']);
$fonteRefatorada = (string) file_get_contents($opcoes['refatorado']);
$metodosOriginais = extrairMetodos($fonteOriginal);
$metodosRefatorados = extrairMetodos($fonteRefatorada);

montarClasse('BoletimOriginal', $metodosOriginais, $metodosOriginais);
montarClasse('BoletimRefatorado', $metodosRefatorados, $metodosOriginais);

[$divergencias, $resultados] = comparar('BoletimOriginal', 'BoletimRefatorado', $casos, $semente);

echo "Teste de equivalência de getSituacaoNotas\n";
echo "Cenários: $casos (semente $semente)\n";
echo 'Métodos auxiliares novos: ' . implode(', ', array_keys(array_diff_key($metodosRefatorados, $metodosOriginais))) . "\n";
echo "Distribuição dos resultados da versão original:\n";
foreach ($resultados as $chave => $qtd) {
    echo "  - $chave: $qtd\n";
}
echo 'Divergências: ' . count($divergencias) . "\n";
foreach (array_slice($divergencias, 0, 5) as $d) {
    echo "  caso {$d['caso']}\n    original:   {$d['original']}\n    refatorado: {$d['refatorado']}\n";
}

$falhou = count($divergencias) > 0;

if (isset($opcoes['autoteste'])) {
    // Defeito injetado: o componente na recuperação aprovado passa a ficar "aprovado" em vez de "aprovado após exame".
    $metodosDefeito = $metodosRefatorados;
    $alvo = '_situacaoComponentePorNota';
    $metodosDefeito[$alvo] = preg_replace(
        '/\$resultado->situacao = App_Model_MatriculaSituacao::APROVADO_APOS_EXAME;/',
        '$resultado->situacao = App_Model_MatriculaSituacao::APROVADO;',
        $metodosDefeito[$alvo],
        1
    );
    montarClasse('BoletimComDefeito', $metodosDefeito, $metodosOriginais);
    [$divDefeito] = comparar('BoletimOriginal', 'BoletimComDefeito', $casos, $semente);
    echo 'Autoteste (defeito injetado): ' . count($divDefeito) . " divergência(s) detectada(s)\n";
    $falhou = $falhou || count($divDefeito) === 0;
}

exit($falhou ? 1 : 0);
