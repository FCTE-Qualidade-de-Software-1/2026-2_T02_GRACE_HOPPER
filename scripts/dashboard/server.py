#!/usr/bin/env python3
"""Servidor HTTP local e somente leitura para o estado do Ralph."""

from __future__ import annotations

import argparse
import json
import re
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

RUN_ID_RE = re.compile(r"^run-[A-Za-z0-9_-]+$")
MAX_LOG_BYTES = 256 * 1024


class RalphStore:
    def __init__(self, repo: Path) -> None:
        self.repo = repo.resolve()
        self.phases = self.repo / ".phases"

    def current_id(self) -> str | None:
        pointer = self.phases / "current"
        try:
            value = pointer.read_text(encoding="utf-8").strip()
        except OSError:
            return None
        return value if RUN_ID_RE.fullmatch(value) else None

    def run_dir(self, run_id: str) -> Path | None:
        if not RUN_ID_RE.fullmatch(run_id):
            return None
        candidate = (self.phases / "runs" / run_id).resolve()
        runs_root = (self.phases / "runs").resolve()
        if candidate.parent != runs_root or not candidate.is_dir():
            return None
        return candidate

    def state_dir(self, run_id: str | None) -> Path | None:
        if run_id:
            run = self.run_dir(run_id)
            return run / "state" if run else None
        legacy = self.phases / "state"
        return legacy if legacy.is_dir() else None

    @staticmethod
    def _read_tsv(path: Path) -> tuple[dict[str, str], list[dict], list[dict]]:
        meta: dict[str, str] = {}
        phases: list[dict] = []
        tasks: list[dict] = []
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return meta, phases, tasks
        for line in lines:
            parts = line.split("\t")
            if not parts:
                continue
            if parts[0] == "META" and len(parts) >= 3:
                meta[parts[1]] = "\t".join(parts[2:])
            elif parts[0] == "PHASE" and len(parts) == 2:
                meta["phase"] = parts[1]
            elif parts[0] == "ACTIVITY" and len(parts) >= 2:
                meta["activity"] = "\t".join(parts[1:])
            elif parts[0] == "PHASE" and len(parts) >= 6:
                phases.append({
                    "number": parts[1], "status": parts[2], "attempt": parts[3],
                    "gates": parts[4].split(), "title": "\t".join(parts[5:]), "tasks": [],
                })
            elif parts[0] == "TASK" and len(parts) >= 5:
                tasks.append({
                    "phase": parts[1], "number": parts[2], "status": parts[3],
                    "title": "\t".join(parts[4:]),
                })
        phase_index = {phase["number"]: phase for phase in phases}
        for task in tasks:
            phase = phase_index.get(task["phase"])
            if phase:
                phase["tasks"].append(task)
        return meta, phases, tasks

    @staticmethod
    def _read_live(path: Path) -> tuple[dict[str, str], list[dict]]:
        meta: dict[str, str] = {}
        tasks: list[dict] = []
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return meta, tasks
        for line in lines:
            parts = line.split("\t")
            if parts[0] == "PHASE" and len(parts) >= 2:
                meta["phase"] = parts[1]
            elif parts[0] == "ACTIVITY" and len(parts) >= 2:
                meta["activity"] = "\t".join(parts[1:])
            elif parts[0] == "LIVE" and len(parts) >= 3:
                tasks.append({"number": parts[1], "status": parts[2]})
        return meta, tasks

    def run_state(self, run_id: str | None = None) -> dict:
        resolved_id = run_id or self.current_id()
        state_dir = self.state_dir(resolved_id)
        if state_dir is None:
            return {"version": 1, "run": None, "phases": [], "updated_at": int(time.time())}
        meta, phases, _ = self._read_tsv(state_dir / "run.tsv")
        live_meta, live_tasks = self._read_live(state_dir / "live.tsv")
        for key in ("activity",):
            if key in live_meta and live_meta[key]:
                meta[key] = live_meta[key]
        phase_number = live_meta.get("phase")
        if phase_number:
            by_phase = {phase["number"]: phase for phase in phases}
            for live_task in live_tasks:
                phase = by_phase.get(phase_number)
                if not phase:
                    continue
                for task in phase["tasks"]:
                    if task["number"] == live_task["number"] and task["status"] not in {"done", "incomplete"}:
                        task["status"] = live_task["status"]
        return {
            "version": 1,
            "run": {"id": resolved_id or meta.get("run"), "meta": meta},
            "phases": phases,
            "updated_at": int(time.time()),
        }

    def runs(self) -> list[dict]:
        runs_root = self.phases / "runs"
        result: list[dict] = []
        if runs_root.is_dir():
            for directory in sorted(runs_root.iterdir(), reverse=True):
                if not directory.is_dir() or not RUN_ID_RE.fullmatch(directory.name):
                    continue
                state = self.run_state(directory.name)
                meta = state["run"]["meta"] if state["run"] else {}
                result.append({"id": directory.name, "project": meta.get("project"), "engine": meta.get("engine"), "status": meta.get("status"), "started": meta.get("started"), "ended": meta.get("ended")})
        current = self.current_id()
        if not result and (self.phases / "state").is_dir():
            legacy = self.run_state(None)
            meta = legacy["run"]["meta"] if legacy["run"] else {}
            result.append({"id": None, "project": meta.get("project"), "engine": meta.get("engine"), "status": meta.get("status"), "started": meta.get("started"), "ended": meta.get("ended")})
        for item in result:
            item["current"] = item["id"] == current
        return result

    def logs(self, run_id: str | None, offset: int) -> dict:
        resolved_id = run_id or self.current_id()
        run = self.run_dir(resolved_id) if resolved_id else None
        log_dir = (run / "logs") if run else (self.phases / "logs")
        try:
            files = sorted(path for path in log_dir.iterdir() if path.is_file())
            data = b"".join(
                b"\n== " + path.name.encode("utf-8", errors="replace") + b" ==\n" + path.read_bytes()
                for path in files
            )
            size = len(data)
            start = max(0, min(offset, size))
            if size - start > MAX_LOG_BYTES:
                start = size - MAX_LOG_BYTES
        except OSError:
            return {"offset": 0, "next_offset": 0, "text": "", "truncated": False}
        chunk = data[start : start + MAX_LOG_BYTES]
        return {"offset": start, "next_offset": start + len(chunk), "text": chunk.decode("utf-8", errors="replace"), "truncated": start > offset}


class Handler(SimpleHTTPRequestHandler):
    store: RalphStore
    assets: Path

    def log_message(self, *_: object) -> None:
        return

    def json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        parts = [unquote(part) for part in parsed.path.split("/") if part]
        if parts[:3] != ["api", "v1", "runs"]:
            return super().do_GET()
        query = parse_qs(parsed.query)
        if len(parts) == 3:
            return self.json({"runs": self.store.runs()})
        run_id = parts[3] if len(parts) >= 4 else None
        if run_id == "current":
            return self.json(self.store.run_state())
        if not RUN_ID_RE.fullmatch(run_id or ""):
            return self.json({"error": "run not found"}, HTTPStatus.NOT_FOUND)
        if len(parts) == 4:
            if not self.store.run_dir(run_id):
                return self.json({"error": "run not found"}, HTTPStatus.NOT_FOUND)
            return self.json(self.store.run_state(run_id))
        if len(parts) == 5 and parts[4] == "logs":
            try:
                offset = max(0, int(query.get("after", ["0"])[0]))
            except ValueError:
                offset = 0
            return self.json(self.store.logs(run_id, offset))
        return self.json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def translate_path(self, path: str) -> str:
        parsed = urlparse(path).path
        if parsed in {"", "/"}:
            return str(self.assets / "index.html")
        target = (self.assets / parsed.lstrip("/")).resolve()
        if target.parent != self.assets.resolve() or not target.is_file():
            return str(self.assets / "missing")
        return str(target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    Handler.store = RalphStore(Path(args.repo))
    Handler.assets = Path(__file__).with_name("web")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
