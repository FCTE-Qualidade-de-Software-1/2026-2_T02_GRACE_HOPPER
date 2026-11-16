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


# ----------------------------------------------------------- Membros da equipe
MEMBROS_EQUIPE = [
    {
        "login": "ArthurDevWorks",
        "nome": "Arthur Soares Parente",
        "matricula": "23/2036770",
        "papel": "Gestão de Configuração e GitPage",
        "trilha_e2": "Trilha A: Docker, Coexistência (M1) e Backup (M6)",
    },
    {
        "login": "fabiofonteles1",
        "nome": "Fábio Santos Araujo",
        "matricula": "22/2022082",
        "papel": "Redação Científica e Comunicação",
        "trilha_e2": "Trilha F: Redação Final, Auditoria e Release E2",
    },
    {
        "login": "Nibaacriba",
        "nome": "Gabriel Barbaceli",
        "matricula": "21/1045122",
        "papel": "GQM Compatibilidade e Interação",
        "trilha_e2": "Trilha B: REST (M2) e Proteção de Interação (M12/M13)",
    },
    {
        "login": "g-srodrigues",
        "nome": "Gustavo Silva Rodrigues",
        "matricula": "23/2036887",
        "papel": "Analista de Qualidade e ISO/IEC 25010",
        "trilha_e2": "Trilha C: Confiabilidade, Oráculo (M3) e Falhas (M4/M5)",
    },
    {
        "login": "ItaloSamP",
        "nome": "Ítalo Alves Sampaio de Oliveira",
        "matricula": "23/2037937",
        "papel": "Arquitetura e Stakeholders",
        "trilha_e2": "Trilha D: Análise Estática (M7-M10) e Testabilidade (M11)",
    },
    {
        "login": "ChickRicks",
        "nome": "Ricardo Lucas Winchello Vieira Branco",
        "matricula": "22/1008409",
        "papel": "Revisão Cruzada e Validação",
        "trilha_e2": "Trilha E: Qualidade em Uso (M14/M15) e Julgamento (IQM)",
    },
]


# ------------------------------------------------------------- Tempo de ciclo
def tempo_ciclo(dados: dict) -> dict:
    concluidas = [i for i in dados["issues"] if i.get("fechada_em")]
    itens = []
    for i in concluidas:
        d_criada = data(i["criada_em"])
        d_fechada = data(i["fechada_em"])
        dias = (d_fechada - d_criada).total_seconds() / 86400.0 if d_criada and d_fechada else 0.0
        if dias > 10.0:
            situacao = "Investigar"
        elif dias < 2.0:
            situacao = "Entrega rápida"
        else:
            situacao = "Dentro do esperado"
        itens.append({
            "numero": i["numero"],
            "titulo": i["titulo"],
            "responsaveis": i.get("responsaveis", []),
            "criada_em": d_criada,
            "fechada_em": d_fechada,
            "dias": round(dias, 1),
            "situacao": situacao,
        })
    itens.sort(key=lambda x: x["numero"])
    media = sum(x["dias"] for x in itens) / len(itens) if itens else 0.0
    return {
        "issues": itens,
        "total_concluidas": len(itens),
        "media_dias": round(media, 1),
        "minimo_dias": min((x["dias"] for x in itens), default=0.0),
        "maximo_dias": max((x["dias"] for x in itens), default=0.0),
        "faixa_esperada": "3,0 a 10,0 dias",
    }


# -------------------------------------------------------------- Contribuições
def contribuicoes(dados: dict) -> dict:
    contribuidores_map = dados.get("contribuidores", {})
    prs_por_autor: dict[str, int] = {}
    prs_integrados_por_autor: dict[str, int] = {}
    for p in dados.get("prs", []):
        autor = p.get("autor")
        if autor:
            prs_por_autor[autor] = prs_por_autor.get(autor, 0) + 1
            if p.get("integrado_em"):
                prs_integrados_por_autor[autor] = prs_integrados_por_autor.get(autor, 0) + 1

    total_fechadas = len([i for i in dados["issues"] if i.get("fechada_em")])
    membros_resumo = []
    total_horas_reais = 0.0
    total_horas_est = 0.0

    for m in MEMBROS_EQUIPE:
        login = m["login"]
        commits = contribuidores_map.get(login, 0)
        prs_abertos = prs_por_autor.get(login, 0)
        prs_integrados = prs_integrados_por_autor.get(login, 0)

        issues_membro = [i for i in dados["issues"] if login in i.get("responsaveis", [])]
        issues_fechadas = [i for i in issues_membro if i.get("fechada_em")]
        issues_abertas = [i for i in issues_membro if not i.get("fechada_em")]

        h_est = sum(i["horas_estimadas"] for i in issues_membro if i.get("horas_estimadas"))
        h_real = sum(i["horas_realizadas"] for i in issues_fechadas if i.get("horas_realizadas") is not None)

        total_horas_reais += h_real
        total_horas_est += h_est

        custo_planejado = 600.0  # Linha de base PC1: 12h @ R$ 50/h
        custo_realizado = h_real * VALOR_HORA
        desvio_custo = custo_realizado - custo_planejado

        membros_resumo.append({
            "login": login,
            "nome": m["nome"],
            "matricula": m["matricula"],
            "papel": m["papel"],
            "trilha_e2": m["trilha_e2"],
            "commits": commits,
            "prs_abertos": prs_abertos,
            "prs_integrados": prs_integrados,
            "issues_atribuidas": len(issues_membro),
            "issues_fechadas": len(issues_fechadas),
            "issues_abertas": len(issues_abertas),
            "horas_estimadas": h_est,
            "horas_realizadas": h_real,
            "horas_consolidadas_e1": 12.0,
            "custo_planejado": custo_planejado,
            "custo_realizado": custo_realizado,
            "desvio_custo": desvio_custo,
        })

    for mr in membros_resumo:
        mr["pct_horas_reais"] = (mr["horas_realizadas"] / total_horas_reais) if total_horas_reais else 0.0
        mr["pct_issues_fechadas"] = (mr["issues_fechadas"] / total_fechadas) if total_fechadas else 0.0

    return {
        "membros": membros_resumo,
        "total_horas_reais": total_horas_reais,
        "total_horas_realizadas": total_horas_reais,
        "total_horas_estimadas": total_horas_est,
        "total_commits": sum(mr["commits"] for mr in membros_resumo),
        "total_prs": len(dados.get("prs", [])),
        "total_fechadas": total_fechadas,
    }


# ---------------------------------------------------- Histórico de medições
def historico_medicoes(dados: dict) -> list[dict]:
    return [
        {
            "data": "27/10/2026",
            "ponto": "Medição 1 — Fechamento PC1 / Release E1",
            "id": "CP-1",
            "indicador": "TCM — Conclusão por Milestone",
            "valor": "19/19 (100,0%)",
            "limite": "TCM < 90% exige redistribuição",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "27/10/2026",
            "ponto": "Medição 1 — Fechamento PC1 / Release E1",
            "id": "CP-2",
            "indicador": "ACM — Aderência ao Calendário",
            "valor": "n/c (marcos sem due date inicial)",
            "limite": "Atraso > 2 dias aciona revisão de escopo",
            "situacao": "Alerta",
        },
        {
            "data": "27/10/2026",
            "ponto": "Medição 1 — Fechamento PC1 / Release E1",
            "id": "RC-1",
            "indicador": "VEC — Variação de Esforço e Custo",
            "valor": "0,0% (55h / 55h em 14 issues)",
            "limite": "|VEC| > 25% exige recalibração",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "27/10/2026",
            "ponto": "Medição 1 — Fechamento PC1 / Release E1",
            "id": "DP-1",
            "indicador": "TRCD — Revisão e Build Estrito",
            "valor": "9/11 (81,8%) global · 9/9 (100%) pós-CI",
            "limite": "TRCD pós-workflow < 100% bloqueia merge",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "27/10/2026",
            "ponto": "Medição 1 — Fechamento PC1 / Release E1",
            "id": "DP-2",
            "indicador": "Tempo de Ciclo Médio",
            "valor": "7,7 dias (19 issues fechadas)",
            "limite": "Média fora de 3 a 10 dias investigar",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "10/11/2026",
            "ponto": "Medição 2 — Transição e Abertura E2",
            "id": "CP-1",
            "indicador": "TCM — Conclusão por Milestone",
            "valor": "19/31 (61,3%) acumulado",
            "limite": "Abertura planejada de 12 issues da E2",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "10/11/2026",
            "ponto": "Medição 2 — Transição e Abertura E2",
            "id": "RC-1",
            "indicador": "VEC — Variação de Esforço e Custo",
            "valor": "0,0% (55h / 55h em 14 issues)",
            "limite": "5 issues fechadas sem registro de horas reais",
            "situacao": "Investigar",
        },
        {
            "data": "10/11/2026",
            "ponto": "Medição 2 — Transição e Abertura E2",
            "id": "DP-1",
            "indicador": "TRCD — Revisão e Build Estrito",
            "valor": "17/19 (89,5%) global · 17/17 (100%) pós-CI",
            "limite": "TRCD pós-workflow < 100% bloqueia merge",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "12/11/2026",
            "ponto": "Medição 3 — Execução da Entrega 2",
            "id": "CP-1",
            "indicador": "TCM — Conclusão por Milestone",
            "valor": "19/31 (61,3%)",
            "limite": "TCM < 50% na metade da E2 aciona replanejamento",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "12/11/2026",
            "ponto": "Medição 3 — Execução da Entrega 2",
            "id": "RC-1",
            "indicador": "VEC — Variação de Esforço e Custo",
            "valor": "-34,3% nas issues com apontamento (71h / 108h)",
            "limite": "|VEC| > 25% exige auditoria de apontamento",
            "situacao": "Investigar",
        },
        {
            "data": "12/11/2026",
            "ponto": "Medição 3 — Execução da Entrega 2",
            "id": "DP-1",
            "indicador": "TRCD — Revisão e Build Estrito",
            "valor": "21/23 (91,3%) global · 21/21 (100%) pós-CI",
            "limite": "TRCD pós-workflow < 100% bloqueia merge",
            "situacao": "Dentro do esperado",
        },
        {
            "data": "12/11/2026",
            "ponto": "Medição 3 — Execução da Entrega 2",
            "id": "DP-2",
            "indicador": "Aprovação Prévia de PRs",
            "valor": "22/23 (95,7%) dos PRs integrados",
            "limite": "Aprovação por par obrigatória antes do merge",
            "situacao": "Dentro do esperado",
        },
    ]


def calcular(dados: dict) -> dict:
    return {
        "tcm": tcm(dados),
        "trcd": trcd(dados),
        "acm": acm(dados),
        "vec": vec(dados),
        "desvios": desvios_prazo(dados),
        "serie": serie_semanal(dados),
        "tempo_ciclo": tempo_ciclo(dados),
        "contribuicoes": contribuicoes(dados),
        "historico": historico_medicoes(dados),
    }
