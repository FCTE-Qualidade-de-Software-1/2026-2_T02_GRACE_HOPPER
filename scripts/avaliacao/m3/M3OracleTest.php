<?php

use App\Models\LegacyEvaluationRule;

uses(Avaliacao_Service_TestCommon::class);

$manifest = json_decode(file_get_contents(__DIR__ . '/m3-manifest.json'), true, 512, JSON_THROW_ON_ERROR);

foreach ($manifest['cases'] as $case) {
    test('M3 ' . $case['id'], function () use ($case, $manifest) {
        $input = $case['inputs'];
        $family = $case['family'];
        // This valid model attribute is absent from the legacy helper defaults.
        $this->_regraOptions['qtdCasasDecimais'] = $manifest['numeric_precision'];
        // Only persistence is mocked: table selection and conversion remain real.
        $makeTable = function ($concept, $rows, $normalize = false) {
            $mapper = $this->getCleanMock('TabelaArredondamento_Model_TabelaValorDataMapper');
            $mapper->method('findAll')->willReturn($rows);
            $tableMapper = new TabelaArredondamento_Model_TabelaDataMapper;
            $tableMapper->setTabelaValorDataMapper($mapper);
            $table = new TabelaArredondamento_Model_Tabela([
                'nome' => 'M3 fixture',
                'tipoNota' => $concept ? RegraAvaliacao_Model_Nota_TipoValor::CONCEITUAL : RegraAvaliacao_Model_Nota_TipoValor::NUMERICA,
                'arredondarNota' => 1,
                'normalizarMedia' => $normalize ? 1 : 0,
            ]);
            $table->setDataMapper($tableMapper);
            return $table;
        };
        $this->_setRegraOption('tabelaArredondamento', $makeTable(false, []));
        if (in_array($family, ['arithmetic', 'weighted', 'exam'])) {
            $formula = new FormulaMedia_Model_Formula([
                'id' => 1, 'nome' => 'M3 formula', 'formulaMedia' => $case['rule'],
                'tipoFormula' => $family === 'exam' ? FormulaMedia_Model_TipoFormula::MEDIA_RECUPERACAO : FormulaMedia_Model_TipoFormula::MEDIA_FINAL,
            ]);
            $this->_setRegraOption($family === 'exam' ? 'formulaRecuperacao' : 'formulaMedia', $formula);
            $service = $this->_getServiceInstance();
            $values = ['Se' => array_sum($input['scores']), 'Et' => count($input['scores'])];
            foreach ($input['scores'] as $i => $score) { $values['E' . ($i + 1)] = $score; }
            if ($family === 'exam') { $values['Rc'] = $input['exam']; }
            $actual = (new ReflectionMethod($service, '_calculaMedia'))->invoke($service, $values);
            $this->assertEqualsWithDelta($case['expected'], $actual, 1e-9, 'Raw formula result');
            $actual = $service->arredondaMedia($actual, $this->componentes->first()->id);
        } elseif ($family === 'remedial') {
            $rule = new LegacyEvaluationRule;
            $rule->tipo_recuperacao_paralela = LegacyEvaluationRule::PARALLEL_REMEDIAL_PER_STAGE;
            $rule->tipo_calculo_recuperacao_paralela = match ($input['mode']) {
                'average' => LegacyEvaluationRule::PARALLEL_REMEDIAL_AVERAGE_SCORE,
                'sum' => LegacyEvaluationRule::PARALLEL_REMEDIAL_SUM_SCORE,
                default => 0,
            };
            // Keep the Boletim calculation real; supply only the evaluation rule.
            $service = $this->getMockBuilder(Avaliacao_Service_Boletim::class)
                ->disableOriginalConstructor()->onlyMethods(['getEvaluationRule'])->getMock();
            $service->method('getEvaluationRule')->willReturn($rule);
            $actual = $service->calculateStageScore(1, $input['score'], $input['remedial']);
            $this->assertEqualsWithDelta($case['expected'], $actual, 1e-9, 'Stage score');
            $actual = $this->_getServiceInstance()->arredondaMedia($actual, $this->componentes->first()->id);
        } else {
            $rows = [];
            if ($family === 'concept') {
                foreach ($manifest['concept_table'] as [$name, $min, $max]) {
                    $rows[] = new TabelaArredondamento_Model_TabelaValor([
                        'tabelaArredondamento' => 2, 'nome' => $name,
                        'valorMinimo' => $min, 'valorMaximo' => $max,
                    ]);
                }
                $this->_setRegraOption('tipoNota', RegraAvaliacao_Model_Nota_TipoValor::NUMERICACONCEITUAL);
                $this->_setRegraOption('tabelaArredondamentoConceitual', $makeTable(true, $rows, $input['normalize']));
            } elseif ($input['action'] !== 'none') {
                $action = match ($input['action']) {
                    'floor' => TabelaArredondamento_Model_TipoArredondamentoMedia::ARREDONDAR_PARA_NOTA_INFERIOR,
                    'ceil' => TabelaArredondamento_Model_TipoArredondamentoMedia::ARREDONDAR_PARA_NOTA_SUPERIOR,
                    'specific' => TabelaArredondamento_Model_TipoArredondamentoMedia::ARREDONDAR_PARA_NOTA_ESPECIFICA,
                };
                $rows[] = new TabelaArredondamento_Model_TabelaValor([
                    'tabelaArredondamento' => 1, 'nome' => substr((string) $input['value'], 2, 1),
                    'acao' => $action, 'casaDecimalExata' => 5,
                ]);
                $this->_setRegraOption('tabelaArredondamento', $makeTable(false, $rows));
            }
            $service = $this->_getServiceInstance();
            $component = $this->componentes->first()->id;
            if ($input['normalize'] ?? false) {
                // Supply the stage count declared by the oracle, rather than
                // the unrelated academic-year fixture's default stage count.
                fwrite(STDOUT, "\nM3_SETUP " . json_encode([
                    'id' => $case['id'], 'fixture_stages' => $service->getOption('etapas'),
                    'declared_stages' => $input['stages'],
                ]) . "\n");
                $service->setOption('etapas', $input['stages']);
                $this->assertSame($input['stages'], $service->getOption('etapas'));
            }
            if ($family === 'concept') {
                $this->mockDbPreparedQuery([['tipo_nota' => ComponenteSerie_Model_TipoNota::CONCEITUAL]]);
            }
            $actual = ($input['normalize'] ?? false) || ($input['action'] ?? '') === 'none'
                ? $service->arredondaMedia($input['value'], $component)
                : $service->arredondaNota(new Avaliacao_Model_NotaComponente(['nota' => $input['value'], 'componenteCurricular' => $component]));
        }
        fwrite(STDOUT, "\nM3_RESULT " . json_encode(['id' => $case['id'], 'expected' => $case['expected'], 'actual' => $actual]) . "\n");
        if (is_string($case['expected'])) {
            $this->assertSame($case['expected'], $actual);
        } else {
            $this->assertEqualsWithDelta($case['expected'], (float) $actual, 1e-9);
            $this->assertSame(number_format($case['expected'], 1, '.', ''), number_format((float) $actual, 1, '.', ''));
        }
    });
}
