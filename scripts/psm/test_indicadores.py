"""Testes dos cálculos PSM/CID (python3 -m unittest scripts/psm/test_indicadores.py)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import indicadores as ind  # noqa: E402
from coletar_dados import RE_ESTIMADA, RE_REALIZADA, extrair_horas  # noqa: E402


def base():
    return {
        "coletado_em": "2026-11-06T23:00:00+00:00",
        "workflow_criado_em": "2026-10-19T03:00:00Z",
        "milestones": [
            {"numero": 1, "titulo": "M1", "prazo": "2026-10-26T00:00:00Z", "prazo_simulado": False},
            {"numero": 2, "titulo": "M2", "prazo": "2026-11-22", "prazo_simulado": True},
            {"numero": 3, "titulo": "M3", "prazo": None, "prazo_simulado": False},
        ],
        "issues": [
            {"numero": 1, "titulo": "a", "milestone": 1, "criada_em": "2026-10-10T12:00:00Z", "fechada_em": "2026-10-20T12:00:00Z",
             "horas_estimadas": 4.0, "horas_realizadas": 5.0},
            # Fechada às 22h do dia do prazo em Brasília (01h UTC do dia seguinte): ainda no prazo.
            {"numero": 2, "titulo": "b", "milestone": 1, "criada_em": "2026-10-10T12:00:00Z", "fechada_em": "2026-10-27T01:00:00Z",
             "horas_estimadas": 4.0, "horas_realizadas": 3.0},
            {"numero": 3, "titulo": "c", "milestone": 2, "criada_em": "2026-10-28T12:00:00Z", "fechada_em": None,
             "horas_estimadas": 2.0, "horas_realizadas": None},
        ],
        "prs": [
            {"numero": 10, "criado_em": "2026-10-18T12:00:00Z", "integrado_em": "2026-10-18T13:00:00Z",
             "primeira_aprovacao_em": None, "build_executado": False, "build_ok": False},
            {"numero": 11, "criado_em": "2026-10-20T12:00:00Z", "integrado_em": "2026-10-21T12:00:00Z",
             "primeira_aprovacao_em": "2026-10-21T10:00:00Z", "build_executado": True, "build_ok": True},
            {"numero": 12, "criado_em": "2026-10-22T12:00:00Z", "integrado_em": None,
             "primeira_aprovacao_em": None, "build_executado": True, "build_ok": False},
        ],
    }


class TestIndicadores(unittest.TestCase):
    def test_tcm(self):
        r = ind.tcm(base())
        self.assertEqual((r["concluidas"], r["planejadas"]), (2, 3))
        self.assertEqual(r["por_milestone"][2]["abertas"], [3])
        self.assertIsNone(r["por_milestone"][3]["taxa"])

    def test_trcd_ignora_pr_nao_integrado(self):
        r = ind.trcd(base())
        self.assertEqual((r["build_ok"], r["integrados"]), (1, 2))
        self.assertEqual(r["sem_aprovacao"], [10])
        self.assertEqual((r["build_ok_apos_workflow"], r["apos_workflow"]), (1, 1))

    def test_acm_prazo_vale_ate_fim_do_dia_em_brasilia(self):
        r = ind.acm(base())
        self.assertEqual((r["no_prazo"], r["avaliados"]), (1, 1))
        self.assertEqual(r["sem_prazo"], ["M3"])

    def test_vec_so_usa_issues_concluidas_com_dois_registros(self):
        r = ind.vec(base())
        self.assertEqual((r["horas_realizadas"], r["horas_estimadas"]), (8.0, 8.0))
        self.assertEqual(r["taxa"], 0.0)
        self.assertEqual(r["iguais_a_estimativa"], [])

    def test_serie_termina_na_coleta(self):
        s = ind.serie_semanal(base())
        self.assertEqual(s[-1]["data"], ind.data("2026-11-06T23:00:00+00:00"))
        self.assertTrue(all(p["data"].weekday() == 6 for p in s[:-1]))

    def test_extrair_horas(self):
        corpo = ("| **Horas Planejadas / Estimadas** | `4 horas` |\n"
                 "- **Esforço Efetivo Realizado**: [Preencher ao concluir: ex. 4h]\n")
        self.assertEqual(extrair_horas(corpo, RE_ESTIMADA), 4.0)
        self.assertIsNone(extrair_horas(corpo, RE_REALIZADA))
        self.assertEqual(extrair_horas("- **Esforço Efetivo Realizado**: 3,5h", RE_REALIZADA), 3.5)

    def test_tempo_ciclo(self):
        tc = ind.tempo_ciclo(base())
        self.assertEqual(tc["total_concluidas"], 2)
        self.assertGreater(tc["media_dias"], 0)
        self.assertEqual(len(tc["issues"]), 2)

    def test_contribuicoes(self):
        dados = base()
        dados["contribuidores"] = {"ArthurDevWorks": 10}
        dados["issues"][0]["responsaveis"] = ["ArthurDevWorks"]
        c = ind.contribuicoes(dados)
        self.assertEqual(len(c["membros"]), 6)
        arthur = next(m for m in c["membros"] if m["login"] == "ArthurDevWorks")
        self.assertEqual(arthur["commits"], 10)
        self.assertEqual(arthur["issues_fechadas"], 1)

    def test_historico_medicoes(self):
        h = ind.historico_medicoes(base())
        self.assertGreaterEqual(len(h), 5)
        self.assertTrue(any(x["id"] == "CP-1" for x in h))


if __name__ == "__main__":
    unittest.main()
