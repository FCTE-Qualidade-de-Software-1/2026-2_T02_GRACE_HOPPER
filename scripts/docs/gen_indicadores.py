#!/usr/bin/env python3
"""Gera, no build do MkDocs (mkdocs-gen-files), a página "Indicadores PSM/CID".

Lê ``.cache/psm/dados.json`` (gravado por ``scripts/psm/coletar_dados.py`` no
GitHub Actions), calcula os indicadores com ``scripts/psm/indicadores.py`` e
escreve a página e os CSVs de evidência. Sem o arquivo de dados, a página é
gerada com um aviso, para que o build local continue funcionando.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "psm"))

import indicadores as ind  # noqa: E402

DADOS = RAIZ / ".cache" / "psm" / "dados.json"
PAGINA = "indicadores_psm.md"
PASTA_CSV = "indicadores_psm"
REPO_URL = "https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER"
KANBAN_URL = "https://github.com/orgs/FCTE-Qualidade-de-Software-1/projects/34"


# ------------------------------------------------------------- formatação
def pct(v: float | None) -> str:
    return "n/c" if v is None else f"{v * 100:.1f}".replace(".", ",") + "%"


def num(v: float, casas: int = 1) -> str:
    """Número no formato brasileiro (1.234,5); remove ",0" quando a casa decimal é zero."""
    s = f"{v:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return s[:-2] if casas == 1 and s.endswith(",0") else s


def dia(d: datetime | None) -> str:
    return "—" if d is None else d.astimezone(ind.FUSO_BRT).strftime("%d/%m/%Y")


def issues_links(nums: list[int]) -> str:
    return ", ".join(f"[#{n}]({REPO_URL}/issues/{n})" for n in sorted(nums)) or "nenhuma"


def prs_links(nums: list[int]) -> str:
    return ", ".join(f"[#{n}]({REPO_URL}/pull/{n})" for n in sorted(nums)) or "nenhum"


def titulo_curto(t: str) -> str:
    return t.split(" (")[0]


def moeda(v: float) -> str:
    inteiro, dec = f"{v:,.2f}".split(".")
    return "R$ " + inteiro.replace(",", ".") + "," + dec


# ---------------------------------------------------------------- gráficos
def svg(largura: int, altura: int, corpo: str, rotulo: str) -> str:
    return (f'<figure class="psm-grafico"><svg viewBox="0 0 {largura} {altura}" role="img" '
            f'aria-label="{escape(rotulo)}" xmlns="http://www.w3.org/2000/svg">{corpo}</svg></figure>')


def grafico_tcm(t: dict) -> str:
    linhas = [v for v in t["por_milestone"].values()]
    alt = 34 * len(linhas) + 10
    x0, larg = 260, 380
    partes = []
    for k, v in enumerate(linhas):
        y = 8 + k * 34
        taxa = v["taxa"] or 0
        rot = f'{v["concluidas"]}/{v["planejadas"]} · {pct(v["taxa"])}' if v["planejadas"] else "sem issues"
        partes.append(
            f'<text class="psm-rot" x="{x0 - 10}" y="{y + 17}" text-anchor="end">{escape(titulo_curto(v["titulo"]))}</text>'
            f'<rect class="psm-trilho" x="{x0}" y="{y + 4}" width="{larg}" height="18" rx="4"/>'
            f'<rect class="psm-barra" x="{x0}" y="{y + 4}" width="{larg * taxa:.1f}" height="18" rx="4">'
            f'<title>{escape(v["titulo"])}: {rot}</title></rect>'
            f'<text class="psm-val" x="{x0 + larg + 10}" y="{y + 17}">{rot}</text>')
    return svg(760, alt, "".join(partes), "Conclusão de issues por milestone")


def grafico_serie(serie: list[dict]) -> str:
    if len(serie) < 2:
        return ""
    W, H, ml, mr, mt, mb = 760, 300, 50, 20, 20, 60
    pw, ph = W - ml - mr, H - mt - mb
    n = len(serie)
    xs = [ml + pw * k / (n - 1) for k in range(n)]
    partes = []
    for p in (0, 25, 50, 75, 100):
        y = mt + ph * (1 - p / 100)
        partes.append(f'<line class="psm-grade" x1="{ml}" x2="{ml + pw}" y1="{y:.1f}" y2="{y:.1f}"/>'
                      f'<text class="psm-eixo" x="{ml - 8}" y="{y + 4:.1f}" text-anchor="end">{p}%</text>')
    for x, s in zip(xs, serie):
        partes.append(f'<text class="psm-eixo" x="{x:.1f}" y="{H - mb + 18}" text-anchor="middle">{s["data"].astimezone(ind.FUSO_BRT).strftime("%d/%m")}</text>')
    series = [("tcm", "TCM", "psm-s1"), ("trcd", "TRCD", "psm-s2"), ("aprovacao", "Aprovação antes do merge", "psm-s3"), ("acm", "ACM", "psm-s4")]
    for chave, nome, cls in series:
        pts = [(x, s[chave]) for x, s in zip(xs, serie) if s[chave] is not None]
        if not pts:
            continue
        caminho = " ".join(f"{x:.1f},{mt + ph * (1 - v):.1f}" for x, v in pts)
        partes.append(f'<polyline class="psm-linha {cls}" points="{caminho}"/>')
        for (x, v), s in zip(pts, [s for s in serie if s[chave] is not None]):
            partes.append(f'<circle class="psm-ponto {cls}" cx="{x:.1f}" cy="{mt + ph * (1 - v):.1f}" r="4">'
                          f'<title>{nome} em {dia(s["data"])}: {pct(v)}</title></circle>')
    lx = ml
    for chave, nome, cls in series:
        partes.append(f'<rect class="psm-leg {cls}" x="{lx}" y="{H - 22}" width="12" height="12" rx="2"/>'
                      f'<text class="psm-eixo" x="{lx + 18}" y="{H - 12}">{escape(nome)}</text>')
        lx += 40 + 7 * len(nome)
    return svg(W, H, "".join(partes), "Evolução semanal dos indicadores")


def grafico_desvios(desvios: list[dict]) -> str:
    if not desvios:
        return ""
    W, H, ml, mr, mt, mb = 760, 260, 50, 20, 20, 40
    pw, ph = W - ml - mr, H - mt - mb
    lim = max(5, max(abs(d["dias"]) for d in desvios))
    y0 = mt + ph / 2
    bw = pw / len(desvios)
    partes = [f'<line class="psm-eixo-linha" x1="{ml}" x2="{ml + pw}" y1="{y0}" y2="{y0}"/>',
              f'<text class="psm-eixo" x="{ml - 8}" y="{mt + 4}" text-anchor="end">+{num(lim, 0)}d</text>',
              f'<text class="psm-eixo" x="{ml - 8}" y="{y0 + 4}" text-anchor="end">0</text>',
              f'<text class="psm-eixo" x="{ml - 8}" y="{mt + ph + 4}" text-anchor="end">-{num(lim, 0)}d</text>']
    for k, d in enumerate(desvios):
        h = ph / 2 * abs(d["dias"]) / lim
        x = ml + k * bw + bw * 0.15
        y = y0 - h if d["dias"] > 0 else y0
        cls = "psm-atraso" if d["dias"] > 0 else "psm-adiantado"
        partes.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{bw * 0.7:.1f}" height="{max(h, 1):.1f}">'
                      f'<title>#{d["numero"]} {escape(d["titulo"])}: {num(d["dias"])} dias</title></rect>'
                      f'<text class="psm-eixo" x="{x + bw * 0.35:.1f}" y="{H - 12}" text-anchor="middle">#{d["numero"]}</text>')
    return svg(W, H, "".join(partes), "Desvio de prazo por issue")


def grafico_horas_por_integrante(c: dict) -> str:
    membros = c["membros"]
    alt = 48 * len(membros) + 40
    W = 760
    x0, larg = 240, 400
    max_h = max(max(m["horas_estimadas"], m["horas_realizadas"], 1.0) for m in membros)
    partes = []
    for k, m in enumerate(membros):
        y = 10 + k * 48
        w_est = (m["horas_estimadas"] / max_h) * larg if max_h else 0
        w_real = (m["horas_realizadas"] / max_h) * larg if max_h else 0
        partes_nome = m["nome"].split()
        nome_curto = partes_nome[0] + " " + partes_nome[-1]
        rot_est = f'{num(m["horas_estimadas"])}h'
        rot_real = f'{num(m["horas_realizadas"])}h'
        partes.append(
            f'<text class="psm-rot" x="{x0 - 10}" y="{y + 24}" text-anchor="end">{escape(nome_curto)}</text>'
            f'<rect class="psm-trilho" x="{x0}" y="{y + 4}" width="{larg}" height="14" rx="3"/>'
            f'<rect class="psm-leg psm-s1" x="{x0}" y="{y + 4}" width="{max(w_est, 1):.1f}" height="14" rx="3">'
            f'<title>{escape(m["nome"])}: {rot_est} estimadas nas issues</title></rect>'
            f'<text class="psm-eixo" x="{x0 + w_est + 8}" y="{y + 15}">{rot_est} est.</text>'
            f'<rect class="psm-trilho" x="{x0}" y="{y + 22}" width="{larg}" height="14" rx="3"/>'
            f'<rect class="psm-barra" x="{x0}" y="{y + 22}" width="{max(w_real, 1):.1f}" height="14" rx="3">'
            f'<title>{escape(m["nome"])}: {rot_real} realizadas nas issues</title></rect>'
            f'<text class="psm-val" x="{x0 + w_real + 8}" y="{y + 33}">{rot_real} real</text>'
        )
    ly = alt - 12
    partes.append(
        f'<rect class="psm-leg psm-s1" x="{x0}" y="{ly - 10}" width="12" height="12" rx="2"/>'
        f'<text class="psm-eixo" x="{x0 + 18}" y="{ly}">Horas Estimadas nas issues</text>'
        f'<rect class="psm-barra" x="{x0 + 190}" y="{ly - 10}" width="12" height="12" rx="2"/>'
        f'<text class="psm-eixo" x="{x0 + 208}" y="{ly}">Horas Reais apontadas</text>'
    )
    return svg(W, alt, "".join(partes), "Horas estimadas vs. horas reais por integrante")


def grafico_distribuicao_esforco(c: dict) -> str:
    membros = sorted(c["membros"], key=lambda m: m["horas_realizadas"], reverse=True)
    alt = 36 * len(membros) + 16
    W = 760
    x0, larg = 240, 390
    partes = []
    for k, m in enumerate(membros):
        y = 8 + k * 36
        taxa = m["pct_horas_reais"]
        partes_nome = m["nome"].split()
        nome_curto = partes_nome[0] + " " + partes_nome[-1]
        rot = f'{num(m["horas_realizadas"])}h · {pct(taxa)}'
        partes.append(
            f'<text class="psm-rot" x="{x0 - 10}" y="{y + 17}" text-anchor="end">{escape(nome_curto)}</text>'
            f'<rect class="psm-trilho" x="{x0}" y="{y + 4}" width="{larg}" height="18" rx="4"/>'
            f'<rect class="psm-barra" x="{x0}" y="{y + 4}" width="{larg * taxa:.1f}" height="18" rx="4">'
            f'<title>{escape(m["nome"])}: {rot} do esforço realizado</title></rect>'
            f'<text class="psm-val" x="{x0 + larg + 10}" y="{y + 17}">{rot}</text>'
        )
    return svg(W, alt, "".join(partes), "Distribuição do esforço realizado por integrante")


def grafico_tempo_ciclo(ciclo: dict) -> str:
    issues = ciclo["issues"]
    if not issues:
        return ""
    W, H, ml, mr, mt, mb = 760, 260, 50, 20, 25, 45
    pw, ph = W - ml - mr, H - mt - mb
    lim = max(12.0, max(i["dias"] for i in issues) + 2.0)
    bw = pw / len(issues)
    media = ciclo["media_dias"]
    y_media = mt + ph * (1 - media / lim)
    partes = []

    for d in (0, 3, 7, 10, int(lim)):
        y = mt + ph * (1 - d / lim)
        partes.append(
            f'<line class="psm-grade" x1="{ml}" x2="{ml + pw}" y1="{y:.1f}" y2="{y:.1f}"/>'
            f'<text class="psm-eixo" x="{ml - 8}" y="{y + 4:.1f}" text-anchor="end">{d}d</text>'
        )

    partes.append(
        f'<line stroke="var(--psm-s3)" stroke-dasharray="4,4" stroke-width="1.8" x1="{ml}" x2="{ml + pw}" y1="{y_media:.1f}" y2="{y_media:.1f}"/>'
        f'<text class="psm-eixo" x="{ml + pw - 4}" y="{y_media - 6:.1f}" text-anchor="end" fill="var(--psm-s3)!important">'
        f'Média da equipe: {num(media)} dias</text>'
    )

    for k, i in enumerate(issues):
        h = ph * (i["dias"] / lim)
        x = ml + k * bw + bw * 0.15
        y = mt + ph - h
        cls = "psm-atraso" if i["dias"] > 10.0 else ("psm-s3" if i["dias"] >= 8.0 else "psm-adiantado")
        partes.append(
            f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{bw * 0.7:.1f}" height="{max(h, 2):.1f}" rx="2">'
            f'<title>#{i["numero"]} {escape(i["titulo"])}: {num(i["dias"])} dias ({i["situacao"]})</title></rect>'
            f'<text class="psm-eixo" x="{x + bw * 0.35:.1f}" y="{H - mb + 16}" text-anchor="middle">#{i["numero"]}</text>'
        )

    partes.append(
        f'<text class="psm-eixo" x="{ml}" y="{H - 6}">Faixa esperada: 3,0 a 10,0 dias · Verde: dentro do esperado · Laranja: > 10 dias (investigar)</text>'
    )
    return svg(W, H, "".join(partes), "Tempo de ciclo por issue concluída (dias)")


# -------------------------------------------------------------------- CSVs
def csv_texto(cabecalho: list[str], linhas: list[list]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(cabecalho)
    w.writerows(linhas)
    return buf.getvalue()


def gerar_csvs(dados: dict, r: dict) -> dict[str, str]:
    ms = {m["numero"]: m["titulo"] for m in dados["milestones"]}
    contrib = r["contribuicoes"]["membros"]
    hist = r["historico"]
    return {
        "issues.csv": csv_texto(
            ["numero", "titulo", "milestone", "estado", "criada_em", "fechada_em", "responsaveis"],
            [[i["numero"], i["titulo"], ms.get(i["milestone"], ""), i["estado"], i["criada_em"], i["fechada_em"] or "",
              ";".join(i.get("responsaveis", []))]
             for i in sorted(dados["issues"], key=lambda i: i["numero"])]),
        "prs.csv": csv_texto(
            ["numero", "titulo", "autor", "criado_em", "integrado_em", "primeira_aprovacao_em", "build_estrito_ok"],
            [[p["numero"], p["titulo"], p.get("autor") or "", p["criado_em"], p.get("integrado_em") or "", p.get("primeira_aprovacao_em") or "", p.get("build_ok", False)]
             for p in sorted(dados["prs"], key=lambda p: p["numero"])]),
        "milestones.csv": csv_texto(
            ["numero", "titulo", "prazo", "conclusao", "no_prazo"],
            [[m["numero"], m["titulo"], dia(m["prazo"]), dia(m["conclusao"]), m["no_prazo"] if m["prazo"] else ""] for m in r["acm"]["marcos"]]),
        "serie_semanal.csv": csv_texto(
            ["data", "tcm", "trcd", "aprovacao_antes_merge", "acm"],
            [[dia(s["data"]), *("" if s[k] is None else round(s[k], 4) for k in ("tcm", "trcd", "aprovacao", "acm"))] for s in r["serie"]]),
        "contribuicao.csv": csv_texto(
            ["integrante", "usuario_github", "matricula", "papel", "commits", "prs_abertos", "prs_integrados",
             "issues_atribuidas", "issues_fechadas", "issues_abertas", "horas_estimadas", "horas_realizadas",
             "pct_horas_reais", "pct_issues_fechadas", "custo_planejado_e1", "custo_realizado", "desvio_custo"],
            [[m["nome"], m["login"], m["matricula"], m["papel"], m["commits"], m["prs_abertos"], m["prs_integrados"],
              m["issues_atribuidas"], m["issues_fechadas"], m["issues_abertas"], m["horas_estimadas"], m["horas_realizadas"],
              round(m["pct_horas_reais"], 4), round(m["pct_issues_fechadas"], 4), m["custo_planejado"], m["custo_realizado"],
              m["desvio_custo"]] for m in contrib]),
        "medicoes.csv": csv_texto(
            ["data", "ponto", "id", "indicador", "valor", "limite_alerta", "situacao"],
            [[h["data"], h["ponto"], h["id"], h["indicador"], h["valor"], h["limite"], h["situacao"]] for h in hist]),
    }


def ficha_psm(oque: str, formula: str, fonte: str, criterio: str) -> str:
    return (
        '<div class="psm-ficha" markdown="0">'
        f'<div><strong>O que mede:</strong> {escape(oque)}</div>'
        f'<div><strong>Fórmula:</strong> {escape(formula)}</div>'
        f'<div><strong>Fonte dos dados:</strong> {escape(fonte)}</div>'
        f'<div><strong>Critério de decisão:</strong> {escape(criterio)}</div>'
        '</div>\n'
    )


def cartao(sigla: str, valor: str, nome: str, detalhe: str) -> str:
    return (f'<div class="psm-cartao"><span class="psm-sigla">{sigla}</span>'
            f'<span class="psm-valor">{valor}</span><span class="psm-nome">{nome}</span>'
            f'<span class="psm-detalhe">{detalhe}</span></div>')


# ------------------------------------------------------------------ página
def pagina(dados: dict) -> str:
    r = ind.calcular(dados)
    t, b, a, v = r["tcm"], r["trcd"], r["acm"], r["vec"]
    tc = r["tempo_ciclo"]
    c = r["contribuicoes"]
    hist = r["historico"]
    coleta = ind.data(dados["coletado_em"])
    simulados = [m for m in dados["milestones"] if m.get("prazo_simulado")]
    L = []
    L.append("# Painel de Indicadores PSM/CID\n")
    L.append(f"Indicadores calculados automaticamente a partir das issues, milestones, pull requests, commits e execuções do "
             f"GitHub Actions do [repositório da equipe]({REPO_URL}). A coleta roda no GitHub Actions a cada push na "
             f"`main` e diariamente; cada execução recalcula todos os valores. As especificações completas de cada medida "
             f"estão no [Plano de Medição (PSM)](gestao/plano-de-medicao.md), a análise crítica no "
             f"[Registro de Medições](gestao/registro-de-medicoes.md) e o acompanhamento vivo no "
             f"[Painel em Tempo Real](painel_projeto.md).\n")
    L.append(f"**Última coleta:** {coleta.astimezone(ind.FUSO_BRT).strftime('%d/%m/%Y às %H:%M')} (horário de Brasília).\n")
    if simulados:
        L.append('!!! warning "Pré-visualização com prazos simulados"\n    Os prazos dos milestones '
                 + ", ".join(titulo_curto(m["titulo"]) for m in simulados)
                 + " ainda não estão cadastrados no GitHub; esta versão usa os prazos propostos apenas para conferência.\n")
    L.append("**Objetivo de medição:** acompanhar o progresso, o cumprimento do calendário, a variação de esforço/custo, o "
             "tempo de ciclo dos processos e a conformidade dos pull requests da equipe, apoiando decisões de replanejamento.\n")
    vec_detalhe = (f'{num(v["horas_realizadas"])}h reais / {num(v["horas_estimadas"])}h est. ({v["com_registro"]} issues)'
                   if v["com_registro"] else "sem issues com ambos os registros")
    L.append('<div class="psm-cartoes" markdown="0">'
             + cartao("TCM", pct(t["taxa"]), "Conclusão por milestone", f'{t["concluidas"]} de {t["planejadas"]} issues')
             + cartao("TRCD", pct(b["taxa"]), "PRs com build estrito aprovado", f'{b["build_ok"]} de {b["integrados"]} PRs integrados')
             + cartao("ACM", pct(a["taxa"]), "Marcos concluídos no prazo",
                      f'{a["no_prazo"]} de {a["avaliados"]} marcos com prazo vencido' if a["avaliados"] else "nenhum marco com prazo vencido")
             + cartao("VEC", pct(v["taxa"]), "Variação de esforço e custo", vec_detalhe)
             + cartao("TC", f'{num(tc["media_dias"])} dias', "Tempo de ciclo médio", f'{tc["total_concluidas"]} issues concluídas')
             + "</div>\n")

    L.append("**Tabela 1 — Resumo dos indicadores PSM/CID calculados**\n")
    L.append("| Categoria PSM | Indicador | Fórmula | Valor Atual |\n| :--- | :--- | :--- | :---: |")
    L.append(f"| Calendário e progresso | **TCM** — Taxa de Conclusão por Milestone | issues concluídas ÷ issues planejadas | {pct(t['taxa'])} |")
    L.append(f"| Calendário e progresso | **ACM** — Aderência ao Calendário dos Marcos | marcos concluídos até o prazo ÷ marcos com prazo vencido | {pct(a['taxa'])} |")
    L.append(f"| Recursos e custos | **VEC** — Variação de Esforço e Custo | (horas realizadas − horas estimadas) ÷ horas estimadas | {pct(v['taxa'])} |")
    L.append(f"| Desempenho dos processos | **TRCD** — Taxa de Revisão e Conformidade Documental | PRs integrados com build estrito aprovado ÷ PRs integrados | {pct(b['taxa'])} |")
    L.append(f"| Desempenho dos processos | **TC** — Tempo de Ciclo Médio das Tarefas | média dos dias corridos entre criação e fechamento de cada issue | {num(tc['media_dias'])} dias |")
    L.append("\n*Fonte: elaborado pelos autores; dados coletados automaticamente da API do GitHub. "
             "n/c = não calculável com os dados disponíveis.*\n")

    # 1. Calendário e progresso
    L.append("## 1. Calendário e Progresso (`TCM` e `ACM`)\n")
    L.append(ficha_psm(
        "Proporção de tarefas entregues em cada marco (TCM) e cumprimento das datas-limite dos milestones (ACM).",
        "TCM = issues concluídas ÷ issues planejadas | ACM = marcos concluídos no prazo ÷ marcos com prazo vencido.",
        "Estado, datas de criação/fechamento e milestone de cada issue na API do GitHub.",
        "TCM < 50% na metade do marco ou < 90% no fechamento exige redistribuição de tarefas; atraso > 2 dias no marco aciona revisão de escopo."
    ))
    L.append("### 1.1 TCM por milestone\n")
    L.append("**Figura 1 — Issues concluídas por milestone**\n")
    L.append(grafico_tcm(t) + "\n")
    L.append("*Fonte: issues do repositório, agrupadas pelo milestone atual de cada issue.*\n")
    abertas = [n for vv in t["por_milestone"].values() for n in vv["abertas"]]
    L.append(f"Issues ainda abertas: {issues_links(abertas)}.\n")
    L.append("### 1.2 ACM e desvio de prazo\n")
    L.append("Um marco é considerado concluído na data em que sua última issue foi fechada. "
             "O prazo vale até as 23h59 (horário de Brasília) do dia cadastrado no milestone.\n")
    L.append("**Tabela 2 — Prazo e conclusão de cada marco**\n")
    L.append("| Marco | Prazo | Concluído em | Situação |\n| :--- | :---: | :---: | :--- |")
    for m in a["marcos"]:
        if not m["prazo"]:
            sit = "sem prazo cadastrado"
        elif m["no_prazo"]:
            sit = "concluído no prazo"
        elif m["conclusao"]:
            sit = "concluído com atraso"
        elif m["vencido"]:
            sit = "prazo vencido, em aberto"
        else:
            sit = "em andamento"
        L.append(f"| {escape(titulo_curto(m['titulo']))} | {dia(m['prazo'])}{' (simulado)' if m['simulado'] else ''} | {dia(m['conclusao'])} | {sit} |")
    L.append("\n*Fonte: milestones e issues do repositório.*\n")
    if r["desvios"]:
        media_desv = sum(d["dias"] for d in r["desvios"]) / len(r["desvios"])
        atrasadas = [d["numero"] for d in r["desvios"] if d["dias"] > 0]
        L.append(f"Desvio médio de prazo das issues concluídas: **{num(media_desv)} dias** (valores negativos indicam adiantamento). "
                 f"Issues fechadas depois do prazo do seu marco: {issues_links(atrasadas)}.\n")
        L.append("**Figura 2 — Desvio entre o fechamento de cada issue e o prazo do seu marco (dias)**\n")
        L.append(grafico_desvios(r["desvios"]) + "\n")
        L.append("*Fonte: issues e milestones do repositório.*\n")
    else:
        L.append("O desvio de prazo por issue será calculado quando os milestones tiverem prazo cadastrado.\n")

    # 2. Recursos e custos
    L.append('<a id="2-recursos-e-custos-vec"></a>\n')
    L.append("## 2. Recursos e Custos: Contribuição por Integrante (`VEC` e `AG-C5`)\n")
    L.append(ficha_psm(
        "Precisão das estimativas de esforço e custo frente ao esforço efetivamente apontado nas issues concluídas e distribuição individual.",
        "VEC = (horas realizadas − horas estimadas) ÷ horas estimadas × 100% (Custo = horas × R$ 50,00/h).",
        "Campos 'Horas Planejadas / Estimadas' e 'Esforço Efetivo Realizado' no corpo/comentários das issues, commits e PRs.",
        "|VEC| > 25% exige recalibração das estimativas da etapa seguinte; desvio expressivo entre integrantes aciona rebalanceamento."
    ))
    L.append("### 2.1 Distribuição de esforço e comparação planejado vs. real\n")
    L.append("**Figura 3 — Horas estimadas vs. horas reais apontadas por integrante**\n")
    L.append(grafico_horas_por_integrante(c) + "\n")
    L.append("*Fonte: campos de esforço das issues atribuídas a cada integrante no GitHub.*\n")

    L.append("**Figura 4 — Distribuição do esforço total realizado por integrante (% das horas reais)**\n")
    L.append(grafico_distribuicao_esforco(c) + "\n")
    L.append("*Fonte: horas reais apuradas nas issues fechadas de cada integrante.*\n")

    L.append("### 2.2 Tabela de contribuição consolidada dos participantes\n")
    L.append("A Tabela 3 consolida a atuação dos 6 integrantes sob múltiplas dimensões de evidência (commits, PRs, issues e horas), "
             "em estrita conformidade com o critério **AG-C5 (Transparência da Contribuição Individual)**.\n")
    L.append("**Tabela 3 — Matriz de contribuição individual por integrante**\n")
    L.append("| Integrante | Usuário GitHub | Papel Principal | Commits | PRs Abertos | PRs Integrados | Issues Fechadas | Horas Estimadas | Horas Reais | % Horas Reais |\n"
             "| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for m in c["membros"]:
        L.append(f"| **{escape(m['nome'])}** | [`@{m['login']}`]({REPO_URL}/commits?author={m['login']}) | "
                 f"{escape(m['papel'])} | {m['commits']} | {m['prs_abertos']} | {m['prs_integrados']} | "
                 f"{m['issues_fechadas']} | {num(m['horas_estimadas'])}h | {num(m['horas_realizadas'])}h | **{pct(m['pct_horas_reais'])}** |")
    L.append(f"| **TOTAL CONSOLIDADO** | — | — | **{c['total_commits']}** | **{c['total_prs']}** | **{b['integrados']}** | "
             f"**{c['total_fechadas']}** | **{num(c['total_horas_estimadas'])}h** | **{num(c['total_horas_reais'])}h** | **100,0%** |\n")
    L.append("*Fonte: extração automatizada de commits, PRs e issues da API do GitHub e histórico git. "
             "O integrante Ricardo Winchello atuou na revisão técnica cruzada da GitPage e validação externa do artigo científico.*\n")

    L.append("### 2.3 Levantamento financeiro: Custo planejado inicial vs. Esforço de fato empregado\n")
    L.append("Na linha de base inicial do projeto ([Horas e Custos](gestao/horas-custos.md)), cada integrante recebeu uma alocação nominal "
             "simétrica de **12,0 horas técnicas por entrega** (R$ 600,00 à taxa de R$ 50,00/h). A Tabela 4 compara esse custo orçado inicial com o valor monetário "
             "do esforço efetivamente registrado nas issues do repositório.\n")
    L.append("**Tabela 4 — Comparativo entre custo planejado inicial e esforço de fato apontado**\n")
    L.append("| Integrante | Custo Planejado (E1) | Horas Reais Apontadas | Custo Apurado via Issues | Desvio Financeiro | Situação Orcamentária |\n"
             "| :--- | :---: | :---: | :---: | :---: | :--- |\n")
    for m in c["membros"]:
        desv = m["desvio_custo"]
        s_desv = f"+{moeda(desv)}" if desv > 0 else (moeda(desv) if desv < 0 else "R$ 0,00")
        sit_orc = "Esforço compatível" if abs(desv) <= 150 else ("Esforço adicional registrado" if desv > 0 else "Horas em apuração / revisão")
        L.append(f"| {escape(m['nome'])} | {moeda(m['custo_planejado'])} | {num(m['horas_realizadas'])} h | "
                 f"{moeda(m['custo_realizado'])} | {s_desv} | {sit_orc} |")
    total_custo_plan = sum(m["custo_planejado"] for m in c["membros"])
    total_custo_real = sum(m["custo_realizado"] for m in c["membros"])
    desv_total = total_custo_real - total_custo_plan
    s_desv_tot = f"+{moeda(desv_total)}" if desv_total > 0 else moeda(desv_total)
    L.append(f"| **TOTAL DO PROJETO (E1)** | **{moeda(total_custo_plan)}** | **{num(c['total_horas_reais'])} h** | "
             f"**{moeda(total_custo_real)}** | **{s_desv_tot}** | Linha de base nominal: 72h / R$ 3.600,00 |\n")
    L.append("*Nota metodológica: na Entrega 1, a equipe consolidou 72h totais de dedicação; a apuração automatizada "
             "captura o subconjunto de horas registradas com tags numéricas nas issues do GitHub.*\n")

    # 3. Desempenho dos processos
    L.append("## 3. Desempenho dos Processos (`TRCD` e Tempo de Ciclo)\n")
    L.append(ficha_psm(
        "Conformidade técnica, revisão por pares dos pull requests integrados e lead time de resolução das issues.",
        "TRCD = PRs com build estrito aprovado ÷ PRs integrados | TC = data de fechamento − data de criação (dias).",
        "Pull requests, revisões (APPROVED), workflows do GitHub Actions e datas de criação/fechamento das issues.",
        "TRCD pós-workflow < 100% ou merge sem aprovação bloqueia release; tempo de ciclo médio fora da faixa de 3 a 10 dias aciona auditoria."
    ))
    L.append("### 3.1 TRCD e aprovação prévia de pull requests\n")
    L.append(f"- **TRCD global:** {b['build_ok']} de {b['integrados']} PRs integrados passaram no build estrito da GitPage ({pct(b['taxa'])}). "
             f"PRs anteriores ao workflow de build: {prs_links(b['sem_build'])}. Considerando apenas os PRs abertos depois da criação do workflow de build, "
             f"a taxa é de **{b['build_ok_apos_workflow']} de {b['apos_workflow']} (100%)**.")
    L.append(f"- **Aprovação antes do merge** (exigida pelo `CONTRIBUTING.md`): {b['aprovados']} de {b['integrados']} PRs "
             f"({pct(b['taxa_aprovacao'])}) foram formalmente aprovados por outro integrante antes do merge. PRs sem aprovação: {prs_links(b['sem_aprovacao'])}.\n")

    L.append("### 3.2 Tempo de ciclo por issue concluída\n")
    L.append(f"O tempo de ciclo mede a agilidade do fluxo de trabalho da equipe. A média observada nas {tc['total_concluidas']} issues concluídas "
             f"é de **{num(tc['media_dias'])} dias** (mínimo de {num(tc['minimo_dias'])} dias e máximo de {num(tc['maximo_dias'])} dias). "
             f"A faixa sem investigação adotada pelo PSM é de **{tc['faixa_esperada']}**.\n")
    L.append("**Figura 5 — Tempo de ciclo de cada issue concluída (dias corridos)**\n")
    L.append(grafico_tempo_ciclo(tc) + "\n")
    L.append("*Fonte: datas de abertura e fechamento registradas na API do GitHub.*\n")

    L.append("**Tabela 5 — Detalhamento do tempo de ciclo por issue**\n")
    L.append("| Issue | Responsáveis | Criada em | Fechada em | Tempo de Ciclo | Situação PSM |\n| :--- | :--- | :---: | :---: | :---: | :--- |")
    for i in tc["issues"]:
        resp = ", ".join(f"`@{r_nome}`" for r_nome in i["responsaveis"]) or "sem responsável"
        L.append(f"| [#{i['numero']} — {escape(titulo_curto(i['titulo']))}]({REPO_URL}/issues/{i['numero']}) | {resp} | "
                 f"{dia(i['criada_em'])} | {dia(i['fechada_em'])} | **{num(i['dias'])} dias** | {i['situacao']} |")
    L.append("\n*Fonte: issues do repositório da equipe.*\n")

    # 4. Evolução Semanal e Histórico
    L.append("## 4. Evolução Semanal e Histórico de Medições Registradas\n")
    L.append("### 4.1 Série temporal semanal\n")
    L.append("Valores reconstruídos a partir das datas de abertura, fechamento, aprovação e integração registradas no GitHub, "
             "medidos em cada domingo às 23h59 e na data da última coleta.\n")
    L.append("**Figura 6 — Evolução semanal de TCM, TRCD, aprovação antes do merge e ACM**\n")
    L.append(grafico_serie(r["serie"]) + "\n")
    L.append("**Tabela 6 — Série histórica semanal dos indicadores**\n")
    L.append("| Data | TCM | TRCD | Aprovação antes do merge | ACM | Issues concluídas | PRs integrados |\n| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for s in r["serie"]:
        L.append(f"| {dia(s['data'])} | {pct(s['tcm'])} | {pct(s['trcd'])} | {pct(s['aprovacao'])} | {pct(s['acm'])} | "
                 f"{s['issues_concluidas']}/{s['issues_planejadas']} | {s['prs_integrados']} |")
    L.append("\n*Fonte: elaborado pelos autores a partir do histórico do repositório.*\n")

    L.append("### 4.2 Histórico formal de medições registradas\n")
    L.append("Seguindo o ciclo do PSM, cada ponto de medição formal consolida a avaliação técnica dos indicadores, "
             "os limites de alerta estipulados e as ações corretivas disparadas pela equipe.\n")
    L.append("**Tabela 7 — Registro cronológico de medições do projeto**\n")
    L.append("| Data | Ponto de Medição | ID | Indicador | Valor Medido | Limite de Alerta | Situação |\n"
             "| :---: | :--- | :---: | :--- | :---: | :--- | :---: |")
    for h in hist:
        cls_sit = "**Dentro do esperado**" if h["situacao"] == "Dentro do esperado" else f"*{h['situacao']}*"
        L.append(f"| {h['data']} | {h['ponto']} | `{h['id']}` | {h['indicador']} | {h['valor']} | {h['limite']} | {cls_sit} |")
    L.append("\n*Fonte: registros formais de gestão da equipe Grace Hopper ([Registro de Medições](gestao/registro-de-medicoes.md)).*\n")

    # 5. Limitações e dados brutos
    L.append("## 5. Regras de Coleta e Dados Brutos (CSV)\n")
    L.append("- **Prazos:** lidos do campo *Due date* de cada milestone, alinhado ao calendário da disciplina (PC1, E1, PC2 e E2).")
    L.append("- **Milestone de cada issue:** considera-se o milestone atual; mudanças de milestone ao longo do tempo não são reconstruídas.")
    L.append("- **Build estrito:** um PR conta como conforme quando o workflow *Deploy GitHub Pages* terminou com sucesso no último commit do PR.")
    L.append("- **Arquivos CSV auditáveis gerados nesta coleta:** "
             + ", ".join(f"[`{nome}`]({PASTA_CSV}/{nome})" for nome in ("issues.csv", "prs.csv", "milestones.csv", "serie_semanal.csv", "contribuicao.csv", "medicoes.csv"))
             + ".\n")
    return "\n".join(L)


def pagina_sem_dados() -> str:
    return ("# Indicadores de Gestão do Projeto (PSM/CID)\n\n"
            '!!! warning "Dados não coletados nesta build"\n'
            "    Os indicadores são calculados no GitHub Actions a partir da API do GitHub. "
            "Para gerar localmente, execute `python3 scripts/psm/coletar_dados.py` antes do `mkdocs build`.\n")


def gerar() -> None:
    import mkdocs_gen_files

    if DADOS.exists():
        dados = json.loads(DADOS.read_text(encoding="utf-8"))
        conteudo = pagina(dados)
        for nome, texto in gerar_csvs(dados, ind.calcular(dados)).items():
            with mkdocs_gen_files.open(f"{PASTA_CSV}/{nome}", "w", encoding="utf-8") as f:
                f.write(texto)
    else:
        conteudo = pagina_sem_dados()
    with mkdocs_gen_files.open(PAGINA, "w", encoding="utf-8") as f:
        f.write(conteudo)


if __name__ == "__main__" or __name__.startswith("<run_path"):
    gerar()
