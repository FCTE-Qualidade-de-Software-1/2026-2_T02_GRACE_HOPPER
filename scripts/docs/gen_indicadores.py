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


# -------------------------------------------------------------------- CSVs
def csv_texto(cabecalho: list[str], linhas: list[list]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(cabecalho)
    w.writerows(linhas)
    return buf.getvalue()


def gerar_csvs(dados: dict, r: dict) -> dict[str, str]:
    ms = {m["numero"]: m["titulo"] for m in dados["milestones"]}
    return {
        "issues.csv": csv_texto(
            ["numero", "titulo", "milestone", "estado", "criada_em", "fechada_em", "responsaveis"],
            [[i["numero"], i["titulo"], ms.get(i["milestone"], ""), i["estado"], i["criada_em"], i["fechada_em"] or "",
              ";".join(i["responsaveis"])]
             for i in sorted(dados["issues"], key=lambda i: i["numero"])]),
        "prs.csv": csv_texto(
            ["numero", "titulo", "autor", "criado_em", "integrado_em", "primeira_aprovacao_em", "build_estrito_ok"],
            [[p["numero"], p["titulo"], p["autor"], p["criado_em"], p["integrado_em"] or "", p["primeira_aprovacao_em"] or "", p["build_ok"]]
             for p in sorted(dados["prs"], key=lambda p: p["numero"])]),
        "milestones.csv": csv_texto(
            ["numero", "titulo", "prazo", "conclusao", "no_prazo"],
            [[m["numero"], m["titulo"], dia(m["prazo"]), dia(m["conclusao"]), m["no_prazo"] if m["prazo"] else ""] for m in r["acm"]["marcos"]]),
        "serie_semanal.csv": csv_texto(
            ["data", "tcm", "trcd", "aprovacao_antes_merge", "acm"],
            [[dia(s["data"]), *("" if s[k] is None else round(s[k], 4) for k in ("tcm", "trcd", "aprovacao", "acm"))] for s in r["serie"]]),
    }


def moeda(v: float) -> str:
    inteiro, dec = f"{v:,.2f}".split(".")
    return "R$ " + inteiro.replace(",", ".") + "," + dec


def ficha_psm(oque: str, formula: str, fonte: str, criterio: str) -> str:
    return (
        '<div class="psm-ficha" markdown="0">'
        f'<div><strong>O que mede:</strong> {escape(oque)}</div>'
        f'<div><strong>Fórmula:</strong> {escape(formula)}</div>'
        f'<div><strong>Fonte dos dados:</strong> {escape(fonte)}</div>'
        f'<div><strong>Critério de decisão:</strong> {escape(criterio)}</div>'
        '</div>\n'
    )


# ------------------------------------------------------------------ página
def cartao(sigla: str, valor: str, nome: str, detalhe: str) -> str:
    return (f'<div class="psm-cartao"><span class="psm-sigla">{sigla}</span>'
            f'<span class="psm-valor">{valor}</span><span class="psm-nome">{nome}</span>'
            f'<span class="psm-detalhe">{detalhe}</span></div>')


def pagina(dados: dict) -> str:
    r = ind.calcular(dados)
    t, b, a, v = r["tcm"], r["trcd"], r["acm"], r["vec"]
    coleta = ind.data(dados["coletado_em"])
    simulados = [m for m in dados["milestones"] if m.get("prazo_simulado")]
    L = []
    L.append("# Painel de Indicadores PSM/CID\n")
    L.append(f"Indicadores calculados automaticamente a partir das issues, milestones, pull requests e execuções do "
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
    L.append("**Objetivo de medição:** acompanhar o progresso, o cumprimento do calendário, a variação de esforço/custo e a "
             "conformidade dos pull requests da equipe, apoiando decisões de replanejamento entre as entregas.\n")
    vec_detalhe = (f'{num(v["horas_realizadas"])}h reais / {num(v["horas_estimadas"])}h est. ({v["com_registro"]} issues)'
                   if v["com_registro"] else "sem issues com ambos os registros")
    L.append('<div class="psm-cartoes" markdown="0">'
             + cartao("TCM", pct(t["taxa"]), "Conclusão por milestone", f'{t["concluidas"]} de {t["planejadas"]} issues')
             + cartao("TRCD", pct(b["taxa"]), "PRs com build estrito aprovado", f'{b["build_ok"]} de {b["integrados"]} PRs integrados')
             + cartao("ACM", pct(a["taxa"]), "Marcos concluídos no prazo",
                      f'{a["no_prazo"]} de {a["avaliados"]} marcos com prazo vencido' if a["avaliados"] else "nenhum marco com prazo vencido")
             + cartao("VEC", pct(v["taxa"]), "Variação de esforço e custo", vec_detalhe)
             + "</div>\n")

    L.append("**Tabela 1 — Resumo dos indicadores PSM/CID calculados**\n")
    L.append("| Categoria PSM | Indicador | Fórmula | Valor Atual |\n| :--- | :--- | :--- | :---: |")
    L.append(f"| Calendário e progresso | **TCM** — Taxa de Conclusão por Milestone | issues concluídas ÷ issues planejadas | {pct(t['taxa'])} |")
    L.append(f"| Calendário e progresso | **ACM** — Aderência ao Calendário dos Marcos | marcos concluídos até o prazo ÷ marcos com prazo vencido | {pct(a['taxa'])} |")
    L.append(f"| Recursos e custos | **VEC** — Variação de Esforço e Custo | (horas realizadas − horas estimadas) ÷ horas estimadas | {pct(v['taxa'])} |")
    L.append(f"| Desempenho dos processos | **TRCD** — Taxa de Revisão e Conformidade Documental | PRs integrados com build estrito aprovado ÷ PRs integrados | {pct(b['taxa'])} |")
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
        media = sum(d["dias"] for d in r["desvios"]) / len(r["desvios"])
        atrasadas = [d["numero"] for d in r["desvios"] if d["dias"] > 0]
        L.append(f"Desvio médio de prazo das issues concluídas: **{num(media)} dias** (valores negativos indicam adiantamento). "
                 f"Issues fechadas depois do prazo do seu marco: {issues_links(atrasadas)}.\n")
        L.append("**Figura 2 — Desvio entre o fechamento de cada issue e o prazo do seu marco (dias)**\n")
        L.append(grafico_desvios(r["desvios"]) + "\n")
        L.append("*Fonte: issues e milestones do repositório.*\n")
    else:
        L.append("O desvio de prazo por issue será calculado quando os milestones tiverem prazo cadastrado.\n")

    # 2. Recursos e custos
    L.append("## 2. Recursos e Custos (`VEC`)\n")
    L.append(ficha_psm(
        "Precisão das estimativas de esforço e custo frente ao esforço efetivamente apontado nas issues concluídas.",
        "VEC = (horas realizadas − horas estimadas) ÷ horas estimadas × 100% (Custo = horas × R$ 50,00/h).",
        "Campos 'Horas Planejadas / Estimadas' e 'Esforço Efetivo Realizado' no corpo/comentários das issues do GitHub.",
        "|VEC| > 25% exige recalibração das estimativas da etapa seguinte; issues fechadas sem horas reais exigem auditoria antes da release."
    ))
    L.append("**Tabela 3 — Apuração de esforço e custo nas issues concluídas**\n")
    L.append("| Métrica | Valor Apurado | Observação |\n| :--- | :---: | :--- |")
    L.append(f"| Issues concluídas no repositório | {v['issues_concluidas']} | Total de issues fechadas até a coleta |")
    L.append(f"| Issues concluídas com ambos os registros (estimado e realizado) | {v['com_registro']} | Base de cálculo do VEC |")
    L.append(f"| Esforço estimado (nas {v['com_registro']} issues auditadas) | {num(v['horas_estimadas'])} h | Equivalente a {moeda(v['custo_estimado'])} |")
    L.append(f"| Esforço realizado (nas {v['com_registro']} issues auditadas) | {num(v['horas_realizadas'])} h | Equivalente a {moeda(v['custo_realizado'])} |")
    L.append(f"| **Variação de Esforço e Custo (`VEC`)** | **{pct(v['taxa'])}** | Desvio financeiro de {moeda(v['custo_realizado'] - v['custo_estimado'])} |")
    L.append("\n*Fonte: dados extraídos automaticamente das issues do GitHub (`scripts/psm/coletar_dados.py`). "
             "Para a alocação consolidada por integrante (72h / R$ 3.600,00 na E1 e na E2), consulte [Horas e Custos](gestao/horas-custos.md).*\n")
    L.append(f"- **Issues concluídas sem apontamento de horas reais no corpo da issue:** {issues_links(v['sem_horas_reais'])}.")
    L.append(f"- **Issues com horas reais idênticas às estimadas:** {issues_links(v['iguais_a_estimativa'])}.\n")

    # 3. Desempenho dos processos
    L.append("## 3. Desempenho dos Processos (`TRCD`)\n")
    L.append(ficha_psm(
        "Conformidade técnica e revisão por pares dos pull requests integrados à branch principal.",
        "TRCD = PRs integrados com build estrito aprovado ÷ total de PRs integrados × 100%.",
        "Pull requests, revisões (APPROVED) e execuções do workflow 'Deploy GitHub Pages' na API do GitHub.",
        "TRCD pós-workflow < 100% ou merge sem revisão por par bloqueia a release até auditoria corretiva."
    ))
    L.append(f"- **TRCD global:** {b['build_ok']} de {b['integrados']} PRs integrados passaram no build estrito da GitPage ({pct(b['taxa'])}). "
             f"PRs anteriores ao workflow de build: {prs_links(b['sem_build'])}. Considerando apenas os PRs abertos depois da criação do workflow de build, "
             f"a taxa é de **{b['build_ok_apos_workflow']} de {b['apos_workflow']} (100%)**.")
    L.append(f"- **Aprovação antes do merge** (complemento da TRCD, exigida pelo `CONTRIBUTING.md`): {b['aprovados']} de {b['integrados']} PRs "
             f"({pct(b['taxa_aprovacao'])}) foram aprovados por outro integrante antes de serem integrados. PRs integrados sem aprovação prévia: {prs_links(b['sem_aprovacao'])}.\n")

    # 4. Evolução
    L.append("## 4. Evolução Semanal\n")
    L.append("Valores reconstruídos a partir das datas de abertura, fechamento, aprovação e integração registradas no GitHub, "
             "medidos em cada domingo às 23h59 e na data da última coleta.\n")
    L.append("**Figura 3 — Evolução semanal de TCM, TRCD, aprovação antes do merge e ACM**\n")
    L.append(grafico_serie(r["serie"]) + "\n")
    L.append("**Tabela 4 — Série histórica semanal dos indicadores**\n")
    L.append("| Data | TCM | TRCD | Aprovação antes do merge | ACM | Issues concluídas | PRs integrados |\n| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for s in r["serie"]:
        L.append(f"| {dia(s['data'])} | {pct(s['tcm'])} | {pct(s['trcd'])} | {pct(s['aprovacao'])} | {pct(s['acm'])} | "
                 f"{s['issues_concluidas']}/{s['issues_planejadas']} | {s['prs_integrados']} |")
    L.append("\n*Fonte: elaborado pelos autores a partir do histórico do repositório.*\n")

    # 5. Limitações e registro
    L.append("## 5. Regras de Coleta e Dados Brutos (CSV)\n")
    L.append("- **Prazos:** lidos do campo *Due date* de cada milestone, alinhado ao calendário da disciplina (PC1, E1, PC2 e E2).")
    L.append("- **Milestone de cada issue:** considera-se o milestone atual; mudanças de milestone ao longo do tempo não são reconstruídas.")
    L.append("- **Build estrito:** um PR conta como conforme quando o workflow *Deploy GitHub Pages* terminou com sucesso no último commit do PR.")
    L.append("- **Arquivos CSV auditáveis gerados nesta coleta:** "
             + ", ".join(f"[`{nome}`]({PASTA_CSV}/{nome})" for nome in ("issues.csv", "prs.csv", "milestones.csv", "serie_semanal.csv"))
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


if __name__ in ("__main__", "<run_path>"):
    gerar()
