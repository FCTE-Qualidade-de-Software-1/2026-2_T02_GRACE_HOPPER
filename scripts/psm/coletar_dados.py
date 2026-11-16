#!/usr/bin/env python3
"""Coleta, pela API do GitHub, os dados brutos usados nos indicadores PSM/CID.

Lê milestones, issues (com comentários), pull requests, revisões e execuções do
GitHub Actions do repositório da equipe e grava um JSON normalizado em
``.cache/psm/dados.json``. Não altera nada no GitHub.

Uso:
    GITHUB_TOKEN=... python3 scripts/psm/coletar_dados.py
    python3 scripts/psm/coletar_dados.py --prazos prazos.json   # simula prazos (apenas pré-visualização)

Sem token a API pública permite 60 requisições por hora; com o GITHUB_TOKEN do
GitHub Actions o limite é suficiente para coletas diárias.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_PADRAO = "FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER"
API = "https://api.github.com"
SAIDA_PADRAO = Path(".cache/psm/dados.json")
WORKFLOW_BUILD = "Deploy GitHub Pages"

# Campos de esforço usados nos templates de issue e no CONTRIBUTING.md.
RE_ESTIMADA = re.compile(
    r"(?:Horas\s+Planejadas\s*/\s*Estimadas|Estimativa\s+de\s+Esfor[çc]o)\**\s*[:|]\s*`?\s*([^|\n`]*)",
    re.IGNORECASE,
)
RE_REALIZADA = re.compile(
    r"(?:Horas\s+Efetivamente\s+Realizadas|Horas\s+Efetivas\s+Realizadas|Esfor[çc]o\s+Efetivo\s+Realizado)\**\s*[:|]\s*`?\s*([^|\n`]*)",
    re.IGNORECASE,
)
RE_NUMERO = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*(?:h\b|hora)", re.IGNORECASE)


def extrair_horas(texto: str | None, padrao: re.Pattern) -> float | None:
    """Retorna as horas do último campo preenchido no texto, ou None.

    Campos de template ainda não preenchidos (``[Preencher...]``) são ignorados.
    """
    if not texto:
        return None
    valor = None
    for m in padrao.finditer(texto):
        n = RE_NUMERO.match(m.group(1))
        if n:
            valor = float(n.group(1).replace(",", "."))
    return valor


class Cliente:
    def __init__(self, repo: str, token: str | None):
        self.repo = repo
        self.token = token
        self.requisicoes = 0

    def _get(self, url: str):
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "grace-hopper-psm-coleta",
        })
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        self.requisicoes += 1
        with urllib.request.urlopen(req, timeout=30) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
            link = resp.headers.get("Link", "")
        prox = re.search(r'<([^>]+)>;\s*rel="next"', link)
        return dados, (prox.group(1) if prox else None)

    def todos(self, caminho: str, chave: str | None = None) -> list:
        url = f"{API}/repos/{self.repo}{caminho}"
        itens: list = []
        while url:
            dados, url = self._get(url)
            itens.extend(dados[chave] if chave else dados)
        return itens


def _login(usuario) -> str | None:
    return usuario.get("login") if usuario else None


def coletar(cli: Cliente) -> dict:
    milestones = cli.todos("/milestones?state=all&per_page=100")
    brutos = cli.todos("/issues?state=all&per_page=100")
    pulls = cli.todos("/pulls?state=all&per_page=100")
    execucoes = cli.todos("/actions/runs?per_page=100", chave="workflow_runs")

    issues = []
    for i in brutos:
        if i.get("pull_request"):
            continue
        comentarios = cli.todos(f"/issues/{i['number']}/comments?per_page=100") if i.get("comments") else []
        textos = [i.get("body") or ""] + [c.get("body") or "" for c in comentarios]
        estimada = realizada = None
        for t in textos:  # o registro mais recente prevalece
            estimada = extrair_horas(t, RE_ESTIMADA) or estimada
            realizada = extrair_horas(t, RE_REALIZADA) or realizada
        issues.append({
            "numero": i["number"],
            "titulo": i["title"],
            "estado": i["state"],
            "criada_em": i["created_at"],
            "fechada_em": i.get("closed_at"),
            "milestone": i["milestone"]["number"] if i.get("milestone") else None,
            "labels": [l["name"] for l in i.get("labels", [])],
            "responsaveis": [a["login"] for a in i.get("assignees", [])],
            "horas_estimadas": estimada,
            "horas_realizadas": realizada,
        })

    builds_ok: dict[str, bool] = {}
    for r in execucoes:
        if r.get("name") != WORKFLOW_BUILD:
            continue
        sha = r.get("head_sha")
        builds_ok[sha] = builds_ok.get(sha, False) or r.get("conclusion") == "success"

    prs = []
    for p in pulls:
        revisoes = cli.todos(f"/pulls/{p['number']}/reviews?per_page=100")
        aprovacoes = sorted(r["submitted_at"] for r in revisoes
                            if r.get("state") == "APPROVED" and r.get("submitted_at")
                            and _login(r.get("user")) != _login(p.get("user")))
        sha = p["head"]["sha"]
        prs.append({
            "numero": p["number"],
            "titulo": p["title"],
            "autor": _login(p.get("user")),
            "criado_em": p["created_at"],
            "integrado_em": p.get("merged_at"),
            "fechado_em": p.get("closed_at"),
            "milestone": p["milestone"]["number"] if p.get("milestone") else None,
            "primeira_aprovacao_em": aprovacoes[0] if aprovacoes else None,
            "build_executado": sha in builds_ok,
            "build_ok": builds_ok.get(sha, False),
        })

    contribuidores: dict[str, int] = {}
    try:
        contrib_api = cli.todos("/contributors?per_page=100")
        for c in contrib_api:
            if c.get("login"):
                contribuidores[c["login"]] = c.get("contributions", 0)
    except Exception:
        pass

    import subprocess
    try:
        out = subprocess.check_output(["git", "shortlog", "-sn", "--all"], text=True)
        alias_map = {
            "arthur parente": "ArthurDevWorks",
            "arthurdevworks": "ArthurDevWorks",
            "gustavo rodrigues": "g-srodrigues",
            "italo alves": "ItaloSamP",
            "ítalo alves": "ItaloSamP",
            "gabriel barbaceli": "Nibaacriba",
            "fabio": "fabiofonteles1",
            "fabio araujo": "fabiofonteles1",
        }
        git_counts: dict[str, int] = {}
        for linha in out.strip().splitlines():
            partes = linha.strip().split("\t")
            if len(partes) == 2:
                qtd, nome = int(partes[0].strip()), partes[1].strip().lower()
                login = alias_map.get(nome)
                if login:
                    git_counts[login] = git_counts.get(login, 0) + qtd
        for l, q in git_counts.items():
            contribuidores[l] = max(contribuidores.get(l, 0), q)
    except Exception:
        pass

    return {
        "repositorio": cli.repo,
        "coletado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "milestones": [{
            "numero": m["number"],
            "titulo": m["title"],
            "prazo": m.get("due_on"),
            "prazo_simulado": False,
            "estado": m["state"],
        } for m in milestones],
        "issues": issues,
        "prs": prs,
        "contribuidores": contribuidores,
        "workflow_criado_em": min((r["created_at"] for r in execucoes if r.get("name") == WORKFLOW_BUILD), default=None),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", REPO_PADRAO))
    ap.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    ap.add_argument("--prazos", type=Path, help="JSON {numero_milestone: 'AAAA-MM-DD'} para simular prazos ausentes (pré-visualização)")
    args = ap.parse_args(argv)

    cli = Cliente(args.repo, os.environ.get("GITHUB_TOKEN"))
    try:
        dados = coletar(cli)
    except urllib.error.HTTPError as e:
        print(f"Falha na API do GitHub: {e.code} {e.reason}", file=sys.stderr)
        return 1

    if args.prazos:
        simulados = json.loads(args.prazos.read_text(encoding="utf-8"))
        for m in dados["milestones"]:
            if not m["prazo"] and str(m["numero"]) in simulados:
                m["prazo"] = simulados[str(m["numero"])]
                m["prazo_simulado"] = True

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(dados['issues'])} issues, {len(dados['prs'])} PRs, {len(dados['milestones'])} milestones "
          f"em {cli.requisicoes} requisições -> {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
