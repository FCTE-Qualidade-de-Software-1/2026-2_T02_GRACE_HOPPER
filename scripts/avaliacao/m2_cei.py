#!/usr/bin/env python3
"""M2 (CEI) - executa os 3 criterios de conformidade por endpoint e calcula o CEI.

Le o manifesto e os JSON Schemas congelados em evidencias/g1_compatibilidade/m2_contratos/,
confere o hash SHA-256 registrado em manifesto.sha256 (congelamento previo) e grava o
relatorio em evidencias/g1_compatibilidade/m2_cei_report.json.

Uso: python scripts/avaliacao/m2_cei.py [--base-url URL] [--token TOKEN_SANCTUM]
Requer: jsonschema (pip install jsonschema).
"""
import argparse
import hashlib
import http.cookiejar
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

RAIZ = Path(__file__).resolve().parents[2]
PASTA = RAIZ / "evidencias" / "g1_compatibilidade"
CONTRATOS = PASTA / "m2_contratos"
ACCESS_KEY = "ieducar-access-key"
SECRET_KEY = "ieducar-secret-key"


def sha256(caminho):
    # normaliza fim de linha para o hash independer de core.autocrlf
    return hashlib.sha256(caminho.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def conferir_congelamento():
    esperado = {}
    for linha in (CONTRATOS / "manifesto.sha256").read_text().splitlines():
        h, nome = linha.split()
        esperado[nome.lstrip("*")] = h
    for nome, h in esperado.items():
        atual = sha256(CONTRATOS / nome)
        if atual != h:
            sys.exit(f"ERRO: {nome} difere do hash congelado ({atual} != {h})")
    return esperado


class Cliente:
    def __init__(self, base, token):
        self.base = base
        self.token = token
        self.sessao = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )
        self.sem_sessao = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )

    def login(self):
        self.sessao.open(self.base + "/login", timeout=60).read()
        dados = urllib.parse.urlencode({"login": "admin", "password": "123456789"}).encode()
        self.sessao.open(self.base + "/login", dados, timeout=90).read()

    def chamar(self, ep, query, modo):
        """modo: 'valida' | 'credencial_incorreta'. Retorna (status, content_type, corpo_bytes)."""
        q = dict(query)
        headers = {"Accept": "application/json"}
        abridor = self.sem_sessao
        if ep["auth"] == "access_key":
            q["access_key"] = ACCESS_KEY if modo == "valida" else "chave-incorreta"
            q["secret_key"] = SECRET_KEY if modo == "valida" else "chave-incorreta"
        elif ep["auth"] == "sessao":
            abridor = self.sessao if modo == "valida" else self.sem_sessao
        elif ep["auth"] == "bearer":
            headers["Authorization"] = "Bearer " + (self.token if modo == "valida" else "token-incorreto")
        url = self.base + ep["path"] + ("?" + urllib.parse.urlencode(q) if q else "")
        try:
            r = abridor.open(urllib.request.Request(url, headers=headers), timeout=120)
            return r.status, r.headers.get("Content-Type", ""), r.read(), url
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Content-Type", ""), e.read(), url


def validar(schema, corpo):
    try:
        dados = json.loads(corpo)
    except Exception as exc:  # corpo nao e JSON (ex.: HTML)
        return False, [f"corpo nao e JSON valido: {type(exc).__name__}"]
    erros = [e.message[:160] for e in Draft202012Validator(schema).iter_errors(dados)]
    return not erros, erros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://localhost:8080")
    ap.add_argument("--token", required=True)
    args = ap.parse_args()

    hashes = conferir_congelamento()
    manifesto = json.loads((CONTRATOS / "manifesto_endpoints.json").read_text(encoding="utf-8"))
    schemas = json.loads((CONTRATOS / "contratos_json_schema.json").read_text(encoding="utf-8"))["schemas"]

    cli = Cliente(args.base_url, args.token)
    cli.login()

    relatorio = {
        "metrica": "M2 - CEI",
        "executado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
        "commit_ieducar": "7903a3efc7689942ee700007f86ed581023aad27",
        "hashes_congelados": hashes,
        "endpoints": [],
    }

    for ep in manifesto["endpoints"]:
        r = {"id": ep["id"], "modulo": ep["modulo"], "metodo": ep["metodo"], "path": ep["path"], "casos": {}}

        # Caso 1 e 2: requisicao valida
        st, ct, corpo, url = cli.chamar(ep, ep["query"], "valida")
        c1 = st == 200 and ct.lower().startswith("application/json")
        c2, erros = validar(schemas[ep["schema"]], corpo) if c1 else (False, ["C1 reprovado; corpo nao avaliado como contrato"])
        r["casos"]["C1_valida_http_json"] = {"ok": c1, "status": st, "content_type": ct}
        r["casos"]["C2_aderencia_schema"] = {"ok": c2, "schema": ep["schema"], "erros": erros, "amostra": corpo[:200].decode("utf-8", "replace")}

        # Caso 3: requisicoes invalidas (P1 parametro ausente; P2 credencial incorreta)
        sondas = {}
        if ep["obrigatorios"]:
            q = {k: v for k, v in ep["query"].items() if k not in ep["obrigatorios"]}
            sondas["P1_parametro_ausente"] = (q, "valida")
        sondas["P2_credencial_incorreta"] = (ep["query"], "credencial_incorreta")
        c3_total = True
        r["casos"]["C3_erro_estruturado"] = {}
        for nome, (q, modo) in sondas.items():
            st, ct, corpo, _ = cli.chamar(ep, q, modo)
            json_ok = ct.lower().startswith("application/json")
            estruturado = json_ok and validar(schemas[ep["erro"]], corpo)[0]
            ok = st < 500 and json_ok and estruturado
            c3_total &= ok
            r["casos"]["C3_erro_estruturado"][nome] = {
                "ok": ok, "status": st, "content_type": ct,
                "amostra": corpo[:160].decode("utf-8", "replace"),
            }
        r["casos"]["C3_erro_estruturado"]["ok"] = c3_total
        r["conforme"] = bool(c1 and c2 and c3_total)
        relatorio["endpoints"].append(r)
        print(f"{ep['id']} {ep['path']} {ep['query'].get('resource', '')}: "
              f"C1={c1} C2={c2} C3={c3_total} -> {'CONFORME' if r['conforme'] else 'NAO CONFORME'}")

    testados = len(relatorio["endpoints"])
    conformes = sum(1 for e in relatorio["endpoints"] if e["conforme"])
    cei = None if testados == 0 else round(100.0 * conformes / testados, 2)
    relatorio["resumo"] = {
        "N_testados": testados, "N_conformes": conformes, "CEI_percentual": cei,
        "H1_2_confirmada_CEI_ge_85": (cei is not None and cei >= 85.0),
    }
    saida = PASTA / "m2_cei_report.json"
    saida.write_text(json.dumps(relatorio, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nN_testados={testados} N_conformes={conformes} CEI={cei}%  -> {saida}")


if __name__ == "__main__":
    main()
