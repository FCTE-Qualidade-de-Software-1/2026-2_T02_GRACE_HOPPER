#!/usr/bin/env python3
"""Avaliação e Auditoria de Capacidade de Interação: Gate M12 (IPPE) e M13 (ADMV).

Processa o catálogo congelado de cenários inválidos (Issue #45) em
``evidencias/g4_interacao_uso/m12_catalogo/catalogo_cenarios_m12.json``,
verifica a integridade criptográfica SHA-256 e gera os contratos de evidência
conforme os padrões ISO/IEC 25010:2023, ISO/IEC 25040:2024 e o Framework GQM:

* Gate M12 (IPPE) — Índice de Proteção contra Erros do Usuário:
  IPPE = (N_cenarios_bloqueados_amigavelmente / N_cenarios_submetidos) * 100%
  Gate binário eliminatório: Aprovado se IPPE == 100%; Bloqueado se < 100%.

* M13 (ADMV) — Autodescritividade das Mensagens de Validação:
  ADMV = (N_mensagens_com_causa_e_acao / N_mensagens_avaliadas) * 100%
  Dupla auditoria independente por pares com resolução por consenso.

Uso:
    python3 scripts/uso/avaliar_m12_m13.py [--path ./i-educar-src] [--output-dir docs/evidencias/g4_interacao_uso]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


NOMES_NIVEL = {4: "Excelente", 3: "Bom", 2: "Regular", 1: "Crítico"}


def verificar_sha256(arquivo_alvo: Path, arquivo_sha: Path) -> bool:
    """Verifica se o hash SHA-256 do arquivo coincide com o manifesto."""
    if not arquivo_alvo.exists() or not arquivo_sha.exists():
        return False
    hash_esperado = arquivo_sha.read_text(encoding="utf-8").split()[0].strip().lower()
    conteudo = arquivo_alvo.read_bytes()
    hash_calculado = hashlib.sha256(conteudo).hexdigest().lower()
    return hash_esperado == hash_calculado


def nivel_m13(admv: float) -> int:
    """Determina o nível ordinal S_i de M13 conforme a Tabela 4 do GQM."""
    if admv >= 98.0:
        return 4
    if admv >= 90.0:
        return 3
    if admv >= 80.0:
        return 2
    return 1


def avaliar_cenarios(catalogo_path: Path, src_path: Path | None = None) -> dict:
    """Carrega o catálogo, valida os cenários e calcula as métricas M12 e M13."""
    if not catalogo_path.exists():
        raise FileNotFoundError(f"Catálogo não encontrado em {catalogo_path}")

    with catalogo_path.open(encoding="utf-8") as f:
        dados = json.load(f)

    cenarios = dados.get("cenarios", [])
    if len(cenarios) < 12:
        raise ValueError(f"O catálogo deve conter ao menos 12 cenários; encontrados {len(cenarios)}.")

    total_submetidos = len(cenarios)
    total_bloqueados = 0
    erros_500 = 0
    persistencias_indesejadas = 0

    mensagens_com_causa = 0
    mensagens_com_acao = 0
    mensagens_totalmente_autodescritivas = 0

    itens_execucao = []

    for c in cenarios:
        cid = c["id"]
        cat = c["categoria"]
        retorno = c["retorno_observado"]
        auditoria = c["auditoria_m13"]["consenso"]

        bloqueio_ok = retorno.get("bloqueio_amigavel", False)
        persistencia = retorno.get("persistencia_indesejada", False)
        erro500 = retorno.get("erro_500_ocorreu", False)
        status_http = retorno.get("status_http", 0)

        if erro500:
            erros_500 += 1
        if persistencia:
            persistencias_indesejadas += 1
        if bloqueio_ok and not persistencia and not erro500 and status_http == 422:
            total_bloqueados += 1

        causa_ok = auditoria.get("informa_causa", False)
        acao_ok = auditoria.get("indica_acao_corretiva", False)

        if causa_ok:
            mensagens_com_causa += 1
        if acao_ok:
            mensagens_com_acao += 1
        if causa_ok and acao_ok:
            mensagens_totalmente_autodescritivas += 1

        itens_execucao.append({
            "id": cid,
            "categoria": cat,
            "titulo": c.get("titulo", ""),
            "status_http": status_http,
            "bloqueio_amigavel": "SIM" if bloqueio_ok else "NÃO",
            "persistencia_banco": "SIM" if persistencia else "NÃO",
            "erro_500": "SIM" if erro500 else "NÃO",
            "mensagem": retorno.get("mensagem_exibida", ""),
            "m13_causa": "SIM" if causa_ok else "NÃO",
            "m13_acao": "SIM" if acao_ok else "NÃO",
            "m13_classificacao": auditoria.get("classificacao", "INDEFINIDO"),
        })

    ippe = (total_bloqueados / total_submetidos) * 100.0
    admv = (mensagens_totalmente_autodescritivas / total_submetidos) * 100.0
    nivel_admv_val = nivel_m13(admv)

    gate_m12_aprovado = (ippe == 100.0)
    hipotese_h41_confirmada = (ippe == 100.0)
    hipotese_h42_confirmada = (80.0 <= admv < 90.0)

    resultado = {
        "metadata": dados.get("metadata", {}),
        "data_apuracao": datetime.now(timezone.utc).isoformat(),
        "m12_gate": {
            "metrica": "M12 — IPPE (Índice de Proteção contra Erros do Usuário)",
            "tipo": "GATE_BINARIO_ELIMINATORIO",
            "total_cenarios_submetidos": total_submetidos,
            "total_cenarios_bloqueados_amigavelmente": total_bloqueados,
            "persistencias_indesejadas": persistencias_indesejadas,
            "erros_500_ocorridos": erros_500,
            "valor_bruto": round(ippe, 4),
            "unidade": "%",
            "criterio_aprovacao": "IPPE == 100%",
            "veredito_gate": "APROVADO" if gate_m12_aprovado else "BLOQUEADO",
            "hipotese_h41": {
                "enunciado": "H4.1: O sistema bloqueia 100% dos cenários inválidos previstos sem persistir dados corrompidos nem retornar erro HTTP 500.",
                "resultado": "Confirmada" if hipotese_h41_confirmada else "Refutada",
            },
        },
        "m13_autodescritividade": {
            "metrica": "M13 — ADMV (Autodescritividade das Mensagens de Validação)",
            "tipo": "METRICA_GRADUAL",
            "total_mensagens_avaliadas": total_submetidos,
            "mensagens_com_causa": mensagens_com_causa,
            "mensagens_com_acao": mensagens_com_acao,
            "mensagens_totalmente_autodescritivas": mensagens_totalmente_autodescritivas,
            "valor_bruto": round(admv, 2),
            "unidade": "%",
            "nivel_ordinal": nivel_admv_val,
            "nivel_rotulo": NOMES_NIVEL[nivel_admv_val],
            "peso_ponderado": 0.8,
            "faixa_referencia": "Regular: [80,0%, 90,0%)",
            "hipotese_h42": {
                "enunciado": "H4.2: Entre 80% e 90% das mensagens informam causa e ação corretiva, com mensagens genéricas residuais no núcleo legado.",
                "resultado": "Confirmada" if hipotese_h42_confirmada else "Refutada",
            },
            "avaliadores": [
                dados.get("metadata", {}).get("responsavel_trilha", "Gabriel Barbaceli (@Nibaacriba)"),
                dados.get("metadata", {}).get("revisor_par", "Ítalo Sampaio (@ItaloSamP)"),
            ],
        },
        "itens": itens_execucao,
    }

    return resultado


def exportar_evidencias(resultado: dict, out_dirs: list[Path]) -> None:
    """Gera m12_ippe.csv, m12_ippe_execucao.log e m13_admv.json nos diretórios de saída."""
    for out_dir in out_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1. m12_ippe.csv
        csv_path = out_dir / "m12_ippe.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id_cenario",
                "categoria",
                "titulo",
                "status_http",
                "bloqueio_amigavel",
                "persistencia_banco",
                "erro_500",
                "mensagem_exibida",
                "m13_causa",
                "m13_acao",
                "m13_classificacao",
            ])
            for it in resultado["itens"]:
                writer.writerow([
                    it["id"],
                    it["categoria"],
                    it["titulo"],
                    it["status_http"],
                    it["bloqueio_amigavel"],
                    it["persistencia_banco"],
                    it["erro_500"],
                    it["mensagem"],
                    it["m13_causa"],
                    it["m13_acao"],
                    it["m13_classificacao"],
                ])

        # 2. m12_ippe_execucao.log e m12_ippe_execucao.txt
        log_content = (
            "=" * 80 + "\n"
            + "RELATÓRIO DE EXECUÇÃO DO GATE M12 (IPPE) E AUDITORIA M13 (ADMV)\n"
            + "=" * 80 + "\n"
            + f"Data de apuração: {resultado['data_apuracao']}\n"
            + f"Commit analisado: {resultado['metadata'].get('commit_congelado', 'N/A')}\n"
            + f"Responsável: {resultado['metadata'].get('responsavel_trilha', 'N/A')}\n"
            + f"Revisor por pares: {resultado['metadata'].get('revisor_par', 'N/A')}\n"
            + "-" * 80 + "\n"
            + "RESULTADOS DOS GATES E MÉTRICAS:\n"
            + f"  • Gate M12 (IPPE): {resultado['m12_gate']['valor_bruto']}% -> {resultado['m12_gate']['veredito_gate']}\n"
            + f"  • Hipótese H4.1: {resultado['m12_gate']['hipotese_h41']['resultado']}\n"
            + f"  • M13 (ADMV): {resultado['m13_autodescritividade']['valor_bruto']}% -> Nível {resultado['m13_autodescritividade']['nivel_rotulo']} (S={resultado['m13_autodescritividade']['nivel_ordinal']})\n"
            + f"  • Hipótese H4.2: {resultado['m13_autodescritividade']['hipotese_h42']['resultado']}\n"
            + "-" * 80 + "\n"
            + "DETALHAMENTO DOS 12 CENÁRIOS SUBMETIDOS:\n"
        )
        for it in resultado["itens"]:
            log_content += (
                f"[{it['id']}] {it['categoria']} - {it['titulo']}\n"
                f"      Status: HTTP {it['status_http']} | Bloqueio amigável: {it['bloqueio_amigavel']} | Persistência indesejada: {it['persistencia_banco']} | Erro 500: {it['erro_500']}\n"
                f"      Mensagem: \"{it['mensagem']}\"\n"
                f"      Auditoria M13: Causa={it['m13_causa']} | Ação={it['m13_acao']} | Classificação={it['m13_classificacao']}\n"
            )
        log_content += "=" * 80 + "\nFIM DO RELATÓRIO DE EVIDÊNCIA M12 / M13\n"

        (out_dir / "m12_ippe_execucao.log").write_text(log_content, encoding="utf-8")
        (out_dir / "m12_ippe_execucao.txt").write_text(log_content, encoding="utf-8")

        # 3. m13_admv.json
        json_path = out_dir / "m13_admv.json"
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalogo",
        type=Path,
        default=Path("evidencias/g4_interacao_uso/m12_catalogo/catalogo_cenarios_m12.json"),
        help="Caminho do catálogo congelado de cenários M12",
    )
    parser.add_argument(
        "--sha",
        type=Path,
        default=Path("evidencias/g4_interacao_uso/m12_catalogo/manifesto.sha256"),
        help="Caminho do manifesto SHA-256 do catálogo",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("./i-educar-src"),
        help="Caminho do repositório i-Educar clonado",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/evidencias/g4_interacao_uso"),
        help="Diretório primário de saída das evidências",
    )
    args = parser.parse_args()

    # 1. Verificar integridade SHA-256
    if not verificar_sha256(args.catalogo, args.sha):
        print(f"ERRO: Falha na validação SHA-256 do catálogo {args.catalogo} frente a {args.sha}.", file=sys.stderr)
        return 1
    print(f"ok   Integridade criptográfica SHA-256 confirmada para {args.catalogo.name}")

    # 2. Avaliar cenários e calcular métricas
    resultado = avaliar_cenarios(args.catalogo, args.path)

    # 3. Exportar evidências para pasta docs/evidencias e evidencias/
    dirs_saida = [args.output_dir, Path("evidencias/g4_interacao_uso")]
    exportar_evidencias(resultado, dirs_saida)

    # 4. Exibir sumário conclusivo
    m12 = resultado["m12_gate"]
    m13 = resultado["m13_autodescritividade"]
    print("=" * 60)
    print("SUMÁRIO DA AVALIAÇÃO DE CAPACIDADE DE INTERAÇÃO (G4):")
    print(f"  • Gate M12 (IPPE): {m12['valor_bruto']}% ({m12['total_cenarios_bloqueados_amigavelmente']}/{m12['total_cenarios_submetidos']}) -> {m12['veredito_gate']}")
    print(f"    Hipótese H4.1: {m12['hipotese_h41']['resultado']}")
    print(f"  • Métrica M13 (ADMV): {m13['valor_bruto']}% ({m13['mensagens_totalmente_autodescritivas']}/{m13['total_mensagens_avaliadas']}) -> Nível {m13['nivel_rotulo']} (S={m13['nivel_ordinal']})")
    print(f"    Hipótese H4.2: {m13['hipotese_h42']['resultado']}")
    print("=" * 60)
    print("Arquivos de evidência gerados com sucesso:")
    for d in dirs_saida:
        print(f"  - {d}/m12_ippe.csv")
        print(f"  - {d}/m12_ippe_execucao.log")
        print(f"  - {d}/m13_admv.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())
