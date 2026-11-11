#!/usr/bin/env python3
"""Calcula M14a, M14b (TMET e razão de tempo) e M15 (TSPT) a partir das fichas das sessões de uso.

Lê os CSVs preenchidos durante as sessões supervisionadas (Issue #46) em
``docs/evidencias/g4_interacao_uso/`` e aplica as fórmulas e faixas do Framework GQM:

* TMET_T = média dos tempos dos participantes que concluíram a tarefa T (minutos);
* R_tempo,T = TMET_T / T_ref,T, com T_ref,T = média de 3 execuções de integrante treinado;
* TSPT = execuções corretas na 1ª submissão / execuções totais x 100%.

Enquanto a coleta não atender ao protocolo (pelo menos 5 participantes P01..P05 com TCLE
e 3 execuções de referência por tarefa), as métricas são reportadas como não mensuráveis.

Uso:
    python3 scripts/uso/calcular_m14_m15.py [--dir docs/evidencias/g4_interacao_uso] [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

DIR_PADRAO = Path("docs/evidencias/g4_interacao_uso")
TAREFAS = ("T1", "T2")
MIN_PARTICIPANTES = 5
EXECUCOES_REFERENCIA = 3
CODIGO = re.compile(r"^P\d{2}$")
NOMES = {4: "Excelente", 3: "Bom", 2: "Regular", 1: "Crítico"}


def ler(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    with caminho.open(encoding="utf-8", newline="") as f:
        return [{k: (v or "").strip() for k, v in linha.items()} for linha in csv.DictReader(f)
                if any((v or "").strip() for v in linha.values())]


def numero(texto: str) -> float:
    return float(texto.replace(",", "."))


def sim(texto: str) -> bool:
    return texto.strip().lower() in {"sim", "s", "1", "true"}


def nivel_razao(r: float) -> int:
    return 4 if r <= 1.5 else 3 if r <= 2.0 else 2 if r <= 3.0 else 1


def nivel_tspt(p: float) -> int:
    return 4 if p >= 90 else 3 if p >= 70 else 2 if p >= 50 else 1


def calcular(pasta: Path) -> dict:
    referencia = ler(pasta / "m14_tempo_referencia.csv")
    tempos = ler(pasta / "m14_tmet.csv")
    sucessos = ler(pasta / "m15_tspt.csv")
    pendencias: list[str] = []

    participantes = sorted({l["participante"] for l in tempos + sucessos})
    invalidos = [p for p in participantes if not CODIGO.match(p)]
    if invalidos:
        pendencias.append(f"códigos fora do padrão P01..Pnn: {', '.join(invalidos)}")
    sem_tcle = sorted({l["participante"] for l in tempos if not sim(l.get("tcle_assinado", ""))})
    if sem_tcle:
        pendencias.append(f"participantes sem TCLE registrado: {', '.join(sem_tcle)}")
    validos = [p for p in participantes if p not in invalidos and p not in sem_tcle]
    if len(validos) < MIN_PARTICIPANTES:
        pendencias.append(f"{len(validos)} participante(s) válido(s); o protocolo exige pelo menos {MIN_PARTICIPANTES}")

    resultado: dict = {"participantes": validos, "tarefas": {}}
    for tarefa in TAREFAS:
        ref = [numero(l["tempo_min"]) for l in referencia if l["tarefa"] == tarefa]
        if len(ref) < EXECUCOES_REFERENCIA:
            pendencias.append(f"{tarefa}: {len(ref)} execução(ões) de referência; são necessárias {EXECUCOES_REFERENCIA}")
        da_tarefa = [l for l in tempos if l["tarefa"] == tarefa and l["participante"] in validos]
        concluidas = [numero(l["tempo_min"]) for l in da_tarefa if sim(l["concluiu"])]
        t_ref = sum(ref) / len(ref) if ref else None
        tmet = sum(concluidas) / len(concluidas) if concluidas else None
        razao = tmet / t_ref if tmet is not None and t_ref else None
        resultado["tarefas"][tarefa] = {
            "t_ref_min": t_ref, "execucoes_referencia": len(ref),
            "participantes": len(da_tarefa), "concluiram": len(concluidas),
            "tmet_min": tmet, "r_tempo": razao,
        }

    execucoes = [l for l in sucessos if l["participante"] in validos and l["tarefa"] in TAREFAS]
    corretas = [l for l in execucoes if sim(l["sucesso_1a_submissao"])]
    tspt = len(corretas) / len(execucoes) * 100 if execucoes else None

    mensuravel = not pendencias
    metricas = {}
    for sigla, tarefa in (("M14a", "T1"), ("M14b", "T2")):
        r = resultado["tarefas"][tarefa]["r_tempo"]
        metricas[sigla] = {"valor": round(r, 3) if mensuravel and r is not None else None}
        if mensuravel and r is not None:
            s = nivel_razao(r)
            metricas[sigla].update({"S": s, "faixa": NOMES[s]})
    metricas["M15"] = {"valor": round(tspt, 1) if mensuravel and tspt is not None else None,
                       "execucoes": len(execucoes), "corretas": len(corretas)}
    if mensuravel and tspt is not None:
        s = nivel_tspt(tspt)
        metricas["M15"].update({"S": s, "faixa": NOMES[s]})

    hipoteses = {}
    if mensuravel and None not in (metricas["M14a"]["valor"], metricas["M14b"]["valor"]):
        ok = all(1.5 < metricas[m]["valor"] <= 2.5 for m in ("M14a", "M14b"))
        hipoteses["H4.3"] = "Confirmada" if ok else "Refutada"
    if mensuravel and metricas["M15"]["valor"] is not None:
        hipoteses["H4.4"] = "Confirmada" if 70 <= metricas["M15"]["valor"] < 90 else "Refutada"

    resultado.update({
        "status": "executado" if mensuravel else "nao_mensuravel",
        "pendencias": pendencias,
        "metricas": metricas,
        "hipoteses": hipoteses,
    })
    return resultado


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", type=Path, default=DIR_PADRAO)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    r = calcular(args.dir)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"Situação: {r['status']}")
    for p in r["pendencias"]:
        print(f"  - pendência: {p}")
    for tarefa, t in r["tarefas"].items():
        print(f"{tarefa}: T_ref={t['t_ref_min']} min | TMET={t['tmet_min']} min | "
              f"concluíram {t['concluiram']}/{t['participantes']} | R_tempo={t['r_tempo']}")
    for sigla, m in r["metricas"].items():
        print(f"{sigla}: {m['valor']} {m.get('faixa', '')}")
    for h, v in r["hipoteses"].items():
        print(f"{h}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
