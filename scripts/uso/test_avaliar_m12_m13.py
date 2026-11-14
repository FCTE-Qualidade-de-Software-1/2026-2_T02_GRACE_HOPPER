"""Testes unitários da avaliação de Gate M12 (IPPE) e M13 (ADMV).

Execução:
    python3 -m unittest scripts/uso/test_avaliar_m12_m13.py
"""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from avaliar_m12_m13 import (  # noqa: E402
    avaliar_cenarios,
    exportar_evidencias,
    nivel_m13,
    verificar_sha256,
)


class TestAvaliarM12M13(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.catalogo_path = Path("evidencias/g4_interacao_uso/m12_catalogo/catalogo_cenarios_m12.json")
        self.sha_path = Path("evidencias/g4_interacao_uso/m12_catalogo/manifesto.sha256")
        self.capturas_dir = Path("evidencias/g4_interacao_uso/capturas_m12")
        self.src_path = Path("i-educar-src")

    def test_verificar_sha256_valido(self):
        self.assertTrue(verificar_sha256(self.catalogo_path, self.sha_path))

    def test_verificar_sha256_invalido(self):
        fake_file = self.temp_dir / "fake.json"
        fake_file.write_text("conteudo adulterado", encoding="utf-8")
        fake_sha = self.temp_dir / "fake.sha256"
        fake_sha.write_text("0123456789abcdef  fake.json\n", encoding="utf-8")
        self.assertFalse(verificar_sha256(fake_file, fake_sha))

    def test_nivel_m13_faixas(self):
        self.assertEqual(nivel_m13(99.0), 4)  # Excelente (>= 98%)
        self.assertEqual(nivel_m13(98.0), 4)
        self.assertEqual(nivel_m13(92.5), 3)  # Bom [90%, 98%)
        self.assertEqual(nivel_m13(90.0), 3)
        self.assertEqual(nivel_m13(83.33), 2)  # Regular [80%, 90%)
        self.assertEqual(nivel_m13(80.0), 2)
        self.assertEqual(nivel_m13(75.0), 1)  # Crítico (< 80%)
        self.assertEqual(nivel_m13(50.0), 1)

    def test_avaliacao_catalogo_oficial(self):
        resultado = avaliar_cenarios(
            self.catalogo_path,
            src_path=self.src_path,
            capturas_dir=self.capturas_dir,
        )

        # M12 Gate Binário
        m12 = resultado["m12_gate"]
        self.assertEqual(m12["total_cenarios_submetidos"], 12)
        self.assertEqual(m12["total_cenarios_bloqueados_amigavelmente"], 12)
        self.assertEqual(resultado["capturas_verificadas"], 12)
        self.assertEqual(m12["persistencias_indesejadas"], 0)
        self.assertEqual(m12["erros_500_ocorridos"], 0)
        self.assertEqual(m12["valor_bruto"], 100.0)
        self.assertEqual(m12["veredito_gate"], "APROVADO")
        self.assertEqual(m12["hipotese_h41"]["resultado"], "Confirmada")

        # M13 Autodescritividade
        m13 = resultado["m13_autodescritividade"]
        self.assertEqual(m13["total_mensagens_avaliadas"], 12)
        self.assertEqual(m13["mensagens_com_causa"], 12)
        self.assertEqual(m13["mensagens_com_acao"], 9)
        self.assertEqual(m13["mensagens_totalmente_autodescritivas"], 9)
        self.assertEqual(m13["valor_bruto"], 75.0)
        self.assertEqual(m13["nivel_ordinal"], 1)
        self.assertEqual(m13["nivel_rotulo"], "Crítico")
        self.assertEqual(m13["hipotese_h42"]["resultado"], "Refutada")

    def test_catalogo_com_falha_em_gate(self):
        # Cria catálogo sintético com 1 cenário retornando erro 500
        with self.catalogo_path.open(encoding="utf-8") as f:
            dados = json.load(f)

        dados["cenarios"][0]["retorno_observado"]["erro_500_ocorreu"] = True
        dados["cenarios"][0]["retorno_observado"]["bloqueio_amigavel"] = False
        fake_cat = self.temp_dir / "catalogo_falha.json"
        fake_cat.write_text(json.dumps(dados), encoding="utf-8")

        res = avaliar_cenarios(
            fake_cat,
            src_path=self.src_path,
            capturas_dir=self.capturas_dir,
        )
        m12 = res["m12_gate"]
        self.assertEqual(m12["total_cenarios_bloqueados_amigavelmente"], 11)
        self.assertLess(m12["valor_bruto"], 100.0)
        self.assertEqual(m12["veredito_gate"], "BLOQUEADO")
        self.assertEqual(m12["hipotese_h41"]["resultado"], "Refutada")

    def test_exportar_evidencias(self):
        resultado = avaliar_cenarios(
            self.catalogo_path,
            src_path=self.src_path,
            capturas_dir=self.capturas_dir,
        )
        out_dir = self.temp_dir / "evidencias_teste"
        exportar_evidencias(resultado, [out_dir])

        self.assertTrue((out_dir / "m12_ippe.csv").exists())
        self.assertTrue((out_dir / "m12_ippe_execucao.log").exists())
        self.assertTrue((out_dir / "m13_admv.json").exists())

        # Verifica conteúdo do CSV
        linhas_csv = (out_dir / "m12_ippe.csv").read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(linhas_csv), 13)  # Cabeçalho + 12 cenários

    def test_path_inexistente_falha(self):
        with self.assertRaises(FileNotFoundError):
            avaliar_cenarios(
                self.catalogo_path,
                src_path=self.temp_dir / "nao_existe",
                capturas_dir=self.capturas_dir,
            )

    def test_captura_ausente_bloqueia_gate(self):
        empty_capturas = self.temp_dir / "capturas_vazias"
        empty_capturas.mkdir()
        res = avaliar_cenarios(
            self.catalogo_path,
            src_path=self.src_path,
            capturas_dir=empty_capturas,
        )
        m12 = res["m12_gate"]
        self.assertEqual(res["capturas_verificadas"], 0)
        self.assertEqual(m12["veredito_gate"], "BLOQUEADO")
        self.assertEqual(m12["hipotese_h41"]["resultado"], "Refutada")


if __name__ == "__main__":
    unittest.main()
