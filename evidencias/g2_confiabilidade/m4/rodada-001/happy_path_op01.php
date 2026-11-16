<?php
// Happy path do OP-01 — Boletim::save() SEM injeção
// Executado via tinker (bootstrap Laravel + legado)
// NÃO altera nenhum arquivo do produto

$matriculaId = 3;
$componenteId = 8;   // primeiro componente via escola_serie_disciplina (escola 2, série 6)
$etapa = 1;

echo "\n=== OP-01 HAPPY PATH ===\n";
echo "matricula={$matriculaId} componente={$componenteId} etapa={$etapa}\n\n";

// Snapshot BEFORE
$before = [
    'nota_aluno'         => DB::table('modules.nota_aluno')->count(),
    'nota_componente'    => DB::table('modules.nota_componente_curricular')->count(),
    'falta_aluno'        => DB::table('modules.falta_aluno')->count(),
    'parecer_aluno'      => DB::table('modules.parecer_aluno')->count(),
    'matricula_aprovado' => DB::table('pmieducar.matricula')->where('cod_matricula', $matriculaId)->value('aprovado'),
];
echo "BEFORE:\n";
foreach ($before as $k => $v) echo "  {$k} = {$v}\n";

try {
    $service = new Avaliacao_Service_Boletim(['matricula' => $matriculaId]);
    echo "\n[1] Boletim instanciado\n";
    echo "  etapaAtual = " . var_export($service->getOption('etapaAtual'), true) . "\n";
    echo "  etapas     = " . var_export($service->getOption('etapas'), true) . "\n";
    echo "  ref_cod_turma = " . var_export($service->getOption('ref_cod_turma'), true) . "\n";

    // Adiciona nota
    $nota = new Avaliacao_Model_NotaComponente([
        'componenteCurricular' => $componenteId,
        'etapa' => $etapa,
        'nota' => 8.5,
    ]);
    $service->addNota($nota);
    echo "\n[2] Nota adicionada (componente {$componenteId}, etapa {$etapa}, nota 8.5)\n";

    // Adiciona falta (mesmo componente, pois usa _componenteCurricularId do último addNota)
    $falta = new Avaliacao_Model_FaltaComponente([
        'componenteCurricular' => $componenteId,
        'etapa' => $etapa,
        'quantidade' => 2,
    ]);
    $service->addFalta($falta);
    echo "[3] Falta adicionada (componente {$componenteId}, etapa {$etapa}, 2 faltas)\n";

    // Chama save() — 4 escritas sequenciais sem transação
    $service->save();
    echo "\n[4] save() executado com SUCESSO\n";

} catch (Throwable $e) {
    echo "\n[ERRO] " . get_class($e) . ": " . $e->getMessage() . "\n";
    echo "  em " . $e->getFile() . ":" . $e->getLine() . "\n";
    if (method_exists($e, 'getPrevious') && $e->getPrevious()) {
        $p = $e->getPrevious();
        echo "  causado por " . get_class($p) . ": " . $p->getMessage() . "\n";
        echo "  em " . $p->getFile() . ":" . $p->getLine() . "\n";
    }
}

// Snapshot AFTER
$after = [
    'nota_aluno'         => DB::table('modules.nota_aluno')->count(),
    'nota_componente'    => DB::table('modules.nota_componente_curricular')->count(),
    'falta_aluno'        => DB::table('modules.falta_aluno')->count(),
    'parecer_aluno'      => DB::table('modules.parecer_aluno')->count(),
    'matricula_aprovado' => DB::table('pmieducar.matricula')->where('cod_matricula', $matriculaId)->value('aprovado'),
];

echo "\nAFTER:\n";
foreach ($after as $k => $v) echo "  {$k} = {$v}\n";

echo "\nDIFF:\n";
$mudou = false;
foreach ($before as $k => $v) {
    $d = $after[$k] - $v;
    if ($d !== 0) {
        echo "  {$k}: {$v} → {$after[$k]} (Δ {$d})\n";
        $mudou = true;
    }
}
if (!$mudou) echo "  (nada mudou — happy path NÃO escreveu nada!)\n";

echo "\n=== FIM ===\n";