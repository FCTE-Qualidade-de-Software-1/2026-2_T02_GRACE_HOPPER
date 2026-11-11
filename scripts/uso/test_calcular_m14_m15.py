"""Testes do cálculo de M14a, M14b e M15 (python3 -m unittest scripts/uso/test_calcular_m14_m15.py).

Os CSVs abaixo são dados sintéticos de teste, criados em pasta temporária; não são evidência de coleta.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from calcular_m14_m15 import calcular  # noqa: E402

REFERENCIA = "tarefa,execucao,executor,tempo_min\nT1,1,X,2\nT1,2,X,2\nT1,3,X,2\nT2,1,X,4\nT2,2,X,4\nT2,3,X,4\n"
CAB_TEMPOS = "participante,tcle_assinado,tarefa,concluiu,tempo_min,observacoes\n"
CAB_SUCESSO = "participante,tarefa,sucesso_1a_submissao,motivo_falha,conferencia_banco\n"


def pasta(referencia: str, tempos: str, sucessos: str) -> Path:
    d = Path(tempfile.mkdtemp())
    (d / "m14_tempo_referencia.csv").write_text(referencia, encoding="utf-8")
    (d / "m14_tmet.csv").write_text(CAB_TEMPOS + tempos, encoding="utf-8")
    (d / "m15_tspt.csv").write_text(CAB_SUCESSO + sucessos, encoding="utf-8")
    return d


def sessoes(n: int, t1: float, t2: float, falhas: int = 0):
    tempos, sucessos = "", ""
    for k in range(1, n + 1):
        p = f"P{k:02d}"
        tempos += f"{p},sim,T1,sim,{t1},\n{p},sim,T2,sim,{t2},\n"
        ok = "nao" if k <= falhas else "sim"
        sucessos += f"{p},T1,{ok},,ok\n{p},T2,sim,,ok\n"
    return tempos, sucessos


class TestM14M15(unittest.TestCase):
    def test_sem_coleta_nao_mensuravel(self):
        r = calcular(pasta("tarefa,execucao,executor,tempo_min\n", "", ""))
        self.assertEqual(r["status"], "nao_mensuravel")
        self.assertIsNone(r["metricas"]["M14a"]["valor"])
        self.assertIsNone(r["metricas"]["M15"]["valor"])
        self.assertEqual(r["hipoteses"], {})

    def test_calculo_completo(self):
        tempos, sucessos = sessoes(5, 4, 8, falhas=2)  # razão 2,0 nas duas tarefas; 8 de 10 corretas
        r = calcular(pasta(REFERENCIA, tempos, sucessos))
        self.assertEqual(r["status"], "executado")
        self.assertEqual(r["metricas"]["M14a"]["valor"], 2.0)
        self.assertEqual(r["metricas"]["M14a"]["S"], 3)
        self.assertEqual(r["metricas"]["M15"]["valor"], 80.0)
        self.assertEqual(r["hipoteses"], {"H4.3": "Confirmada", "H4.4": "Confirmada"})

    def test_menos_de_cinco_participantes(self):
        tempos, sucessos = sessoes(4, 4, 8)
        r = calcular(pasta(REFERENCIA, tempos, sucessos))
        self.assertEqual(r["status"], "nao_mensuravel")

    def test_tmet_ignora_quem_nao_concluiu(self):
        tempos, sucessos = sessoes(5, 4, 8)
        tempos += "P06,sim,T1,nao,30,\n"
        r = calcular(pasta(REFERENCIA, tempos, sucessos))
        self.assertEqual(r["tarefas"]["T1"]["tmet_min"], 4.0)
        self.assertEqual(r["tarefas"]["T1"]["concluiram"], 5)

    def test_participante_sem_tcle_fica_de_fora(self):
        tempos, sucessos = sessoes(5, 4, 8)
        tempos = tempos.replace("P05,sim", "P05,nao")
        r = calcular(pasta(REFERENCIA, tempos, sucessos))
        self.assertEqual(r["status"], "nao_mensuravel")
        self.assertNotIn("P05", r["participantes"])


if __name__ == "__main__":
    unittest.main()
