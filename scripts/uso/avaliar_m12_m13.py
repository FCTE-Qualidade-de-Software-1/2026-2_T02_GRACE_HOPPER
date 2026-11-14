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
import re
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


def _validar_produto_alvo(src_path: Path | None, cenarios: list[dict]) -> Path:
    """Valida a existência real do repositório i-Educar e dos arquivos-alvo citados."""
    if src_path is None or not src_path.exists() or not (src_path / "app").is_dir():
        raise FileNotFoundError(
            f"Diretório-alvo do produto inválido ou ausente: {src_path}. "
            "A auditoria M12/M13 exige o código-fonte real do i-Educar."
        )
    for c in cenarios:
        camada = str(c.get("camada_alvo", ""))
        for rel in re.findall(r"[A-Za-z0-9_./-]+\.php", camada):
            if not (src_path / rel).is_file():
                raise FileNotFoundError(
                    f"Arquivo-alvo citado no cenário {c.get('id')} não encontrado em {src_path}: {rel}"
                )
    return src_path


def _validar_captura_cenario(
    cenario: dict,
    capturas_dir: Path,
) -> tuple[bool, dict]:
    """Valida a captura HTTP/SQL bruta do cenário e sua ligação com a mensagem de M13."""
    cid = cenario["id"]
    retorno = cenario["retorno_observado"]
    evidencia = cenario.get("evidencia_execucao", {})
    m13_origem = cenario.get("auditoria_m13", {}).get("evidencia_origem", {})

    rel_cap = evidencia.get("captura_arquivo") or f"capturas_m12/{cid}.json"
    cap_path = capturas_dir / Path(rel_cap).name
    if not cap_path.is_file():
        return False, {"erro": f"Captura bruta ausente: {cap_path}", "captura_arquivo": str(rel_cap)}

    cap = json.loads(cap_path.read_text(encoding="utf-8"))
    if cap.get("cenario_id") != cid:
        return False, {"erro": f"cenario_id divergente na captura {cap_path.name}", "captura_arquivo": str(rel_cap)}

    resp = cap.get("resposta", {})
    body_raw = resp.get("body_raw")
    sha_esperado = resp.get("sha256_body", "")
    if not isinstance(body_raw, str) or not sha_esperado:
        return False, {"erro": f"Corpo HTTP bruto ou sha256_body ausente em {cap_path.name}", "captura_arquivo": str(rel_cap)}

    sha_calc = hashlib.sha256(body_raw.encode("utf-8")).hexdigest()
    if sha_calc != sha_esperado:
        return False, {"erro": f"SHA-256 divergente no corpo HTTP de {cap_path.name}", "captura_arquivo": str(rel_cap)}

    if evidencia.get("sha256_corpo_resposta") and evidencia["sha256_corpo_resposta"] != sha_calc:
        return False, {"erro": f"sha256_corpo_resposta do catálogo diverge da captura {cap_path.name}", "captura_arquivo": str(rel_cap)}

    sql = cap.get("sql_verificacao", {})
    antes = sql.get("contagem_antes")
    depois = sql.get("contagem_depois")
    if not isinstance(antes, int) or not isinstance(depois, int):
        return False, {"erro": f"Consulta SQL antes/depois ausente em {cap_path.name}", "captura_arquivo": str(rel_cap)}

    persistencia_real = (depois != antes) or bool(sql.get("persistencia_indesejada", False)) or bool(retorno.get("persistencia_indesejada", False))
    status_http = int(resp.get("status_http", 0))
    erro500_real = (status_http >= 500) or bool(retorno.get("erro_500_ocorreu", False))
    msg_cap = cap.get("mensagem_capturada")

    # Validação de bloqueio amigável conforme o endpoint real executado
    bloqueio_http_ok = False
    if isinstance(msg_cap, str) and msg_cap.strip() != "":
        if status_http in (400, 422):
            bloqueio_http_ok = True
        elif status_http == 200:
            try:
                body_json = json.loads(body_raw)
                bloqueio_http_ok = bool(body_json.get("any_error_msg") is True and body_json.get("msgs"))
            except json.JSONDecodeError:
                bloqueio_http_ok = False
        elif status_http == 302:
            bloqueio_http_ok = bool(resp.get("redirect_location")) and resp.get("redirect_follow_status") == 200

    msg_catalogo = retorno.get("mensagem_exibida")
    status_catalogo = int(retorno.get("status_http", 0))
    consistencia_catalogo = (msg_cap == msg_catalogo) and (status_http == status_catalogo)

    # Vínculo obrigatório M13 -> captura bruta
    msg_sha = hashlib.sha256((msg_cap or "").encode("utf-8")).hexdigest()
    vinculo_m13_ok = (
        bool(m13_origem)
        and Path(str(m13_origem.get("captura_arquivo", ""))).name == cap_path.name
        and m13_origem.get("mensagem_capturada") == msg_cap
        and m13_origem.get("mensagem_sha256") == msg_sha
    )

    bloqueio_ok = (
        bool(retorno.get("bloqueio_amigavel", False))
        and bloqueio_http_ok
        and consistencia_catalogo
        and vinculo_m13_ok
        and not persistencia_real
        and not erro500_real
    )

    cap_sha = hashlib.sha256(cap_path.read_bytes()).hexdigest()
    req = cap.get("requisicao", {})
    return bloqueio_ok, {
        "captura_arquivo": str(rel_cap),
        "captura_sha256": cap_sha,
        "requisicao_http": f"{req.get('method', '')} {req.get('url', '')}".strip(),
        "status_http": status_http,
        "sha256_corpo_resposta": sha_calc,
        "mensagem_sha256": msg_sha,
        "vinculo_m13_valido": vinculo_m13_ok,
        "sql_tabela": sql.get("tabela", retorno.get("tabela_banco_conferida", "")),
        "sql_contagem_antes": antes,
        "sql_contagem_depois": depois,
        "sql_delta": depois - antes,
        "persistencia_real": persistencia_real,
        "erro500_real": erro500_real,
        "erro": None if bloqueio_ok else "Falha na verificação de bloqueio amigável, SQL, status HTTP ou vínculo M13",
    }


def avaliar_cenarios(
    catalogo_path: Path,
    src_path: Path | None = Path("./i-educar-src"),
    capturas_dir: Path | None = None,
) -> dict:
    """Carrega o catálogo, valida produto/capturas reais e calcula M12 e M13."""
    if not catalogo_path.exists():
        raise FileNotFoundError(f"Catálogo não encontrado em {catalogo_path}")

    with catalogo_path.open(encoding="utf-8") as f:
        dados = json.load(f)

    cenarios = dados.get("cenarios", [])
    if len(cenarios) < 12:
        raise ValueError(f"O catálogo deve conter ao menos 12 cenários; encontrados {len(cenarios)}.")

    alvo_validado = _validar_produto_alvo(src_path, cenarios)
    if capturas_dir is None:
        capturas_dir = catalogo_path.parent.parent / "capturas_m12"

    total_submetidos = len(cenarios)
    total_bloqueados = 0
    erros_500 = 0
    persistencias_indesejadas = 0
    capturas_validas = 0

    mensagens_com_causa = 0
    mensagens_com_acao = 0
    mensagens_totalmente_autodescritivas = 0

    itens_execucao = []

    for c in cenarios:
        cid = c["id"]
        cat = c["categoria"]
        retorno = c["retorno_observado"]
        auditoria = c["auditoria_m13"]["consenso"]

        bloqueio_efetivo, ev = _validar_captura_cenario(c, capturas_dir)
        persistencia = bool(ev.get("persistencia_real", retorno.get("persistencia_indesejada", False)))
        erro500 = bool(ev.get("erro500_real", retorno.get("erro_500_ocorreu", False)))
        status_http = int(ev.get("status_http", retorno.get("status_http", 0)))

        if ev.get("erro") is None:
            capturas_validas += 1
        if erro500:
            erros_500 += 1
        if persistencia:
            persistencias_indesejadas += 1
        if bloqueio_efetivo:
            total_bloqueados += 1

        causa_ok = bool(auditoria.get("informa_causa", False))
        acao_ok = bool(auditoria.get("indica_acao_corretiva", False))

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
            "requisicao_http": ev.get("requisicao_http", ""),
            "status_http": status_http,
            "bloqueio_amigavel": "SIM" if bloqueio_efetivo else "NÃO",
            "persistencia_banco": "SIM" if persistencia else "NÃO",
            "erro_500": "SIM" if erro500 else "NÃO",
            "mensagem": retorno.get("mensagem_exibida", ""),
            "m13_causa": "SIM" if causa_ok else "NÃO",
            "m13_acao": "SIM" if acao_ok else "NÃO",
            "m13_classificacao": auditoria.get("classificacao", "INDEFINIDO"),
            "captura_arquivo": ev.get("captura_arquivo", ""),
            "captura_sha256": ev.get("captura_sha256", ""),
            "sha256_corpo_resposta": ev.get("sha256_corpo_resposta", ""),
            "mensagem_sha256": ev.get("mensagem_sha256", ""),
            "vinculo_m13_valido": bool(ev.get("vinculo_m13_valido", False)),
            "sql_verificacao": {
                "tabela": ev.get("sql_tabela", ""),
                "contagem_antes": ev.get("sql_contagem_antes"),
                "contagem_depois": ev.get("sql_contagem_depois"),
                "delta": ev.get("sql_delta"),
            },
            "validacao_captura_erro": ev.get("erro"),
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
        "alvo_produto": str(alvo_validado),
        "capturas_dir": str(capturas_dir),
        "capturas_verificadas": capturas_validas,
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
                "requisicao_http",
                "status_http",
                "bloqueio_amigavel",
                "sql_tabela",
                "sql_contagem_antes",
                "sql_contagem_depois",
                "sql_delta",
                "persistencia_banco",
                "erro_500",
                "captura_arquivo",
                "sha256_corpo_resposta",
                "mensagem_exibida",
                "m13_causa",
                "m13_acao",
                "m13_classificacao",
            ])
            for it in resultado["itens"]:
                sql = it.get("sql_verificacao", {})
                writer.writerow([
                    it["id"],
                    it["categoria"],
                    it["titulo"],
                    it.get("requisicao_http", ""),
                    it["status_http"],
                    it["bloqueio_amigavel"],
                    sql.get("tabela", ""),
                    sql.get("contagem_antes", ""),
                    sql.get("contagem_depois", ""),
                    sql.get("delta", ""),
                    it["persistencia_banco"],
                    it["erro_500"],
                    it.get("captura_arquivo", ""),
                    it.get("sha256_corpo_resposta", ""),
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
            + f"Alvo do produto: {resultado.get('alvo_produto', 'N/A')}\n"
            + f"Diretório de capturas: {resultado.get('capturas_dir', 'N/A')}\n"
            + f"Capturas verificadas: {resultado.get('capturas_verificadas', 0)}/{resultado['m12_gate']['total_cenarios_submetidos']}\n"
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
            sql = it.get("sql_verificacao", {})
            log_content += (
                f"[{it['id']}] {it['categoria']} - {it['titulo']}\n"
                f"      Requisição: {it.get('requisicao_http', 'N/A')}\n"
                f"      Status: HTTP {it['status_http']} | Bloqueio amigável: {it['bloqueio_amigavel']} | Persistência indesejada: {it['persistencia_banco']} | Erro 500: {it['erro_500']}\n"
                f"      SQL ({sql.get('tabela', 'N/A')}): antes={sql.get('contagem_antes')} depois={sql.get('contagem_depois')} delta={sql.get('delta')}\n"
                f"      Captura: {it.get('captura_arquivo', '')} (SHA-256 body={it.get('sha256_corpo_resposta', '')})\n"
                f"      Mensagem: \"{it['mensagem']}\"\n"
                f"      Auditoria M13: Causa={it['m13_causa']} | Ação={it['m13_acao']} | Classificação={it['m13_classificacao']} | Vínculo={it.get('vinculo_m13_valido')}\n"
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
        "--capturas-dir",
        type=Path,
        default=Path("evidencias/g4_interacao_uso/capturas_m12"),
        help="Diretório das capturas HTTP/SQL brutas dos 12 cenários",
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

    # 2. Avaliar cenários e calcular métricas (exige produto real e capturas brutas válidas)
    try:
        resultado = avaliar_cenarios(args.catalogo, args.path, args.capturas_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

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
