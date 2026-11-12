"""Cálculo dos indicadores PSM/CID a partir dos dados coletados do GitHub.

Funções puras (sem rede): recebem o dicionário gravado por ``coletar_dados.py``
e devolvem os valores usados na página "Indicadores PSM/CID" da GitPage.

Indicadores (mesmas definições do artigo e do Relatório PC1, seção 3.1):

* TCM  — Taxa de Conclusão por Milestone = issues concluídas / issues planejadas.
* TRCD — Taxa de Revisão e Conformidade Documental = PRs integrados com build
  estrito aprovado / PRs integrados. Complemento: PRs aprovados por outro
  integrante antes do merge.
* ACM  — Aderência ao Calendário dos Marcos = marcos concluídos até o prazo /
  marcos com prazo já vencido. Complemento: desvio de prazo por issue.
* VEC  — Variação de Esforço e Custo = (horas realizadas - horas estimadas) /
  horas estimadas, no conjunto de issues com os dois registros.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

VALOR_HORA = 50.0
FUSO_BRT = timezone(timedelta(hours=-3))


def data(iso: str | None) -> datetime | None:
    if not iso:
        return None
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def prazo_do_marco(iso: str | None) -> datetime | None:
    """Prazo de um milestone como fim do dia (23h59, Brasília).

    O GitHub grava o prazo como uma data à meia-noite UTC; o que vale é o dia.
    """
    if not iso:
        return None
    dia = datetime.strptime(iso[:10], "%Y-%m-%d")
    return dia.replace(hour=23, minute=59, second=59, tzinfo=FUSO_BRT)


def razao(num: float, den: float) -> float | None:
    return num / den if den else None


# --------------------------------------------------------------------- TCM
def tcm(dados: dict, ate: datetime | None = None) -> dict:
    """TCM por milestone e total, considerando o estado até ``ate`` (padrão: agora)."""
    por_ms = {}
    for m in dados["milestones"]:
        planejadas = [i for i in dados["issues"] if i["milestone"] == m["numero"]
                      and (ate is None or data(i["criada_em"]) <= ate)]
        concluidas = [i for i in planejadas if i["fechada_em"]
                      and (ate is None or data(i["fechada_em"]) <= ate)]
        por_ms[m["numero"]] = {
            "titulo": m["titulo"],
            "planejadas": len(planejadas),
            "concluidas": len(concluidas),
            "taxa": razao(len(concluidas), len(planejadas)),
            "abertas": [i["numero"] for i in planejadas if i not in concluidas],
        }
    plan = sum(v["planejadas"] for v in por_ms.values())
    conc = sum(v["concluidas"] for v in por_ms.values())
    return {"por_milestone": por_ms, "planejadas": plan, "concluidas": conc, "taxa": razao(conc, plan)}


# -------------------------------------------------------------------- TRCD
def trcd(dados: dict, ate: datetime | None = None) -> dict:
    integrados = [p for p in dados["prs"] if p["integrado_em"]
                  and (ate is None or data(p["integrado_em"]) <= ate)]
    com_build = [p for p in integrados if p["build_ok"]]
    aprovados = [p for p in integrados if p["primeira_aprovacao_em"]
                 and data(p["primeira_aprovacao_em"]) <= data(p["integrado_em"])]
    apos_workflow = [p for p in integrados if p["build_executado"]]
    return {
        "integrados": len(integrados),
        "build_ok": len(com_build),
        "taxa": razao(len(com_build), len(integrados)),
        "sem_build": [p["numero"] for p in integrados if not p["build_ok"]],
        "aprovados": len(aprovados),
        "taxa_aprovacao": razao(len(aprovados), len(integrados)),
        "sem_aprovacao": [p["numero"] for p in integrados if p not in aprovados],
        "apos_workflow": len(apos_workflow),
        "build_ok_apos_workflow": len([p for p in apos_workflow if p["build_ok"]]),
    }


# --------------------------------------------------------------------- ACM
def conclusao_milestone(dados: dict, numero: int) -> datetime | None:
    """Data em que a última issue do milestone foi fechada (None se há issue aberta ou nenhuma issue)."""
    issues = [i for i in dados["issues"] if i["milestone"] == numero]
    if not issues or any(not i["fechada_em"] for i in issues):
        return None
    return max(data(i["fechada_em"]) for i in issues)


def acm(dados: dict, ate: datetime | None = None) -> dict:
    agora = ate or data(dados["coletado_em"])
    marcos = []
    for m in dados["milestones"]:
        prazo = prazo_do_marco(m["prazo"])
        conclusao = conclusao_milestone(dados, m["numero"])
        if conclusao and conclusao > agora:
            conclusao = None
        vencido = bool(prazo and prazo <= agora)
        no_prazo = bool(prazo and conclusao and conclusao <= prazo)
        marcos.append({
            "numero": m["numero"], "titulo": m["titulo"], "prazo": prazo, "conclusao": conclusao,
            "vencido": vencido, "no_prazo": no_prazo, "simulado": m.get("prazo_simulado", False),
        })
    avaliados = [x for x in marcos if x["vencido"]]
    sem_prazo = [x["titulo"] for x in marcos if not x["prazo"]]
    return {
        "marcos": marcos,
        "avaliados": len(avaliados),
        "no_prazo": len([x for x in avaliados if x["no_prazo"]]),
        "taxa": razao(len([x for x in avaliados if x["no_prazo"]]), len(avaliados)),
        "sem_prazo": sem_prazo,
    }


def desvios_prazo(dados: dict) -> list[dict]:
    """Dias entre o fechamento de cada issue e o prazo do seu milestone (negativo = adiantada)."""
    prazos = {m["numero"]: prazo_do_marco(m["prazo"]) for m in dados["milestones"] if m["prazo"]}
    saida = []
    for i in dados["issues"]:
        prazo = prazos.get(i["milestone"])
        if prazo and i["fechada_em"]:
            dias = (data(i["fechada_em"]) - prazo).total_seconds() / 86400
            saida.append({"numero": i["numero"], "titulo": i["titulo"], "dias": dias})
    return sorted(saida, key=lambda x: x["numero"])


# --------------------------------------------------------------------- VEC
def vec(dados: dict) -> dict:
    concluidas = [i for i in dados["issues"] if i["fechada_em"]]
    com_ambos = [i for i in concluidas if i["horas_estimadas"] and i["horas_realizadas"] is not None]
    est = sum(i["horas_estimadas"] for i in com_ambos)
    real = sum(i["horas_realizadas"] for i in com_ambos)
    identicas = [i["numero"] for i in com_ambos if i["horas_realizadas"] == i["horas_estimadas"]]
    return {
        "issues_concluidas": len(concluidas),
        "com_registro": len(com_ambos),
        "sem_horas_reais": [i["numero"] for i in concluidas if i["horas_realizadas"] is None],
        "horas_estimadas": est,
        "horas_realizadas": real,
        "taxa": razao(real - est, est),
        "custo_estimado": est * VALOR_HORA,
        "custo_realizado": real * VALOR_HORA,
        "iguais_a_estimativa": identicas,
    }


# ----------------------------------------------------------- Série semanal
def domingos(inicio: datetime, fim: datetime) -> list[datetime]:
    """Domingos 23h59 (horário de Brasília) entre ``inicio`` e ``fim``, mais o próprio ``fim``."""
    d = inicio.astimezone(FUSO_BRT)
    d = (d + timedelta(days=(6 - d.weekday()) % 7)).replace(hour=23, minute=59, second=0, microsecond=0)
    pontos = []
    while d < fim:
        pontos.append(d)
        d += timedelta(days=7)
    pontos.append(fim)
    return pontos


def serie_semanal(dados: dict) -> list[dict]:
    criacoes = [data(i["criada_em"]) for i in dados["issues"]] + [data(p["criado_em"]) for p in dados["prs"]]
    if not criacoes:
        return []
    fim = data(dados["coletado_em"])
    serie = []
    for t in domingos(min(criacoes), fim):
        c, r, a = tcm(dados, t), trcd(dados, t), acm(dados, t)
        serie.append({
            "data": t, "tcm": c["taxa"], "trcd": r["taxa"], "aprovacao": r["taxa_aprovacao"], "acm": a["taxa"],
            "issues_concluidas": c["concluidas"], "issues_planejadas": c["planejadas"], "prs_integrados": r["integrados"],
        })
    return serie


def calcular(dados: dict) -> dict:
    return {
        "tcm": tcm(dados), "trcd": trcd(dados), "acm": acm(dados), "vec": vec(dados),
        "desvios": desvios_prazo(dados), "serie": serie_semanal(dados),
    }
