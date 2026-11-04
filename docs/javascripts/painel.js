/*
 * Painel do Projeto em tempo real.
 * Consulta a API pública do GitHub direto no navegador do visitante
 * (sem token) e renderiza milestones, issues e pull requests.
 * Só executa em páginas que contenham o elemento #painel-projeto.
 */
(function () {
  "use strict";

  var REPO = "FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER";
  var REPO_URL = "https://github.com/" + REPO;
  var API = "https://api.github.com/repos/" + REPO;
  var REFRESH_MS = 120000; // 2 min: respeita o limite de 60 req/h sem token
  var CACHE_KEY = "painel-projeto-cache-v1";
  var CACHE_TTL_MS = 60000;
  var MAX_PAGES = 5;
  var RECENT_CLOSED = 10;

  /* Ícones SVG inline (16x16, traço em currentColor). */
  var ICONS = {
    issueOpen: '<circle cx="8" cy="8" r="6.25"/><circle cx="8" cy="8" r="1.25" fill="currentColor"/>',
    issueClosed: '<circle cx="8" cy="8" r="6.25"/><path d="M5.25 8.25l1.9 1.9 3.6-3.9"/>',
    prOpen: '<circle cx="4" cy="3.5" r="1.75"/><circle cx="4" cy="12.5" r="1.75"/><path d="M4 5.25v5.5"/>' +
      '<circle cx="12" cy="12.5" r="1.75"/><path d="M12 10.75V6.5a2 2 0 0 0-2-2H7.5M9 3l-1.5 1.5L9 6"/>',
    merged: '<circle cx="4" cy="3.5" r="1.75"/><circle cx="4" cy="12.5" r="1.75"/><path d="M4 5.25v5.5"/>' +
      '<circle cx="12" cy="9" r="1.75"/><path d="M4 5.25C4 7.5 6.5 9 10.25 9"/>',
    refresh: '<path d="M13.25 8a5.25 5.25 0 1 1-1.54-3.71"/><path d="M13.25 2.5v3h-3"/>',
  };

  function icon(name) {
    return '<svg class="pp-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + ICONS[name] + "</svg>";
  }

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fmtDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleDateString("pt-BR");
  }

  function fmtDateTime(date) {
    return date.toLocaleString("pt-BR");
  }

  var RELATIVE_UNITS = [
    ["year", 31536000], ["month", 2592000], ["week", 604800],
    ["day", 86400], ["hour", 3600], ["minute", 60],
  ];

  /* "há 3 dias", "em 2 semanas"; recorre à data absoluta sem suporte a Intl. */
  function relTime(iso) {
    if (!iso) return "—";
    if (typeof Intl === "undefined" || !Intl.RelativeTimeFormat) return fmtDate(iso);
    var rtf = new Intl.RelativeTimeFormat("pt-BR", { numeric: "auto" });
    var diff = (new Date(iso).getTime() - Date.now()) / 1000;
    for (var i = 0; i < RELATIVE_UNITS.length; i++) {
      var unit = RELATIVE_UNITS[i];
      if (Math.abs(diff) >= unit[1]) return rtf.format(Math.round(diff / unit[1]), unit[0]);
    }
    return rtf.format(0, "second");
  }

  function timeTag(iso) {
    if (!iso) return '<span class="pp-muted">—</span>';
    return '<time datetime="' + esc(iso) + '" title="' + esc(fmtDateTime(new Date(iso))) + '">' +
      esc(relTime(iso)) + "</time>";
  }

  function nextLink(header) {
    if (!header) return null;
    var m = header.match(/<([^>]+)>;\s*rel="next"/);
    return m ? m[1] : null;
  }

  async function fetchAll(path) {
    var url = API + path;
    var items = [];
    for (var page = 0; url && page < MAX_PAGES; page++) {
      var res = await fetch(url, { headers: { Accept: "application/vnd.github+json" } });
      if (!res.ok) {
        var reset = res.headers.get("x-ratelimit-reset");
        var msg = "GitHub API respondeu " + res.status;
        if (res.status === 403 && reset) {
          msg += " (limite de requisições; libera às " +
            new Date(Number(reset) * 1000).toLocaleTimeString("pt-BR") + ")";
        }
        throw new Error(msg);
      }
      var data = await res.json();
      if (!Array.isArray(data)) throw new Error("Resposta inesperada da API");
      items = items.concat(data);
      url = nextLink(res.headers.get("link"));
    }
    return items;
  }

  async function loadData() {
    try {
      var cached = JSON.parse(sessionStorage.getItem(CACHE_KEY) || "null");
      if (cached && Date.now() - cached.at < CACHE_TTL_MS) return cached;
    } catch (e) { /* cache inválido: ignora */ }

    var results = await Promise.all([
      fetchAll("/milestones?state=all&per_page=100&sort=due_on"),
      fetchAll("/issues?state=all&per_page=100&sort=updated&direction=desc"),
    ]);
    var data = { at: Date.now(), milestones: results[0], items: results[1] };
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch (e) { /* quota */ }
    return data;
  }

  function labelChips(labels) {
    if (!labels || !labels.length) return "";
    return '<div class="pp-labels">' + labels.map(function (l) {
      return '<span class="pp-label" style="--pp-label:#' + esc(l.color || "888888") + '">' +
        esc(l.name) + "</span>";
    }).join("") + "</div>";
  }

  function assignees(list) {
    if (!list || !list.length) return '<span class="pp-muted">sem responsável</span>';
    return '<div class="pp-avatars">' + list.map(function (a) {
      return '<a href="' + esc(a.html_url) + '" title="' + esc(a.login) + '">' +
        '<img class="pp-avatar" loading="lazy" src="' + esc(a.avatar_url) + '&s=48" alt="' + esc(a.login) + '"></a>';
    }).join("") + "</div>";
  }

  function sectionTitle(text, count) {
    return '<h2 class="pp-section-title">' + esc(text) +
      (count == null ? "" : ' <span class="pp-count">' + esc(count) + "</span>") + "</h2>";
  }

  function renderToolbar(data) {
    return '<div class="pp-toolbar">' +
      '<div class="pp-source"><span class="pp-live" aria-hidden="true"></span>' +
      '<span>Dados de <a href="' + REPO_URL + '">' + esc(REPO.split("/")[1]) + "</a></span>" +
      '<span class="pp-sep" aria-hidden="true">·</span>' +
      '<span>atualizado às <time datetime="' + esc(new Date(data.at).toISOString()) + '" title="' +
      esc(fmtDateTime(new Date(data.at))) + '">' + esc(new Date(data.at).toLocaleTimeString("pt-BR")) +
      "</time></span></div>" +
      '<button type="button" class="pp-btn pp-refresh">' + icon("refresh") + "<span>Atualizar</span></button>" +
      "</div>";
  }

  function renderCards(issues, prs) {
    var open = issues.filter(function (i) { return i.state === "open"; }).length;
    var closed = issues.length - open;
    var prOpen = prs.filter(function (p) { return p.state === "open"; }).length;
    var prMerged = prs.filter(function (p) { return p.pull_request && p.pull_request.merged_at; }).length;
    var pct = issues.length ? Math.round((closed / issues.length) * 100) : 0;
    var cards = [
      ["Issues abertas", open, "issueOpen", "open"],
      ["Issues fechadas", closed, "issueClosed", "closed"],
      ["PRs abertos", prOpen, "prOpen", "open"],
      ["PRs mergeados", prMerged, "merged", "closed"],
    ];
    return '<div class="pp-cards">' +
      '<div class="pp-card pp-card--ring">' +
      '<div class="pp-ring" style="--pp-pct:' + pct + '" role="img" aria-label="' + pct +
      '% das issues concluídas"><span>' + pct + "%</span></div>" +
      '<div class="pp-card-body"><span class="pp-card-label">Conclusão geral</span>' +
      '<span class="pp-card-sub">' + closed + " de " + issues.length + " issues fechadas</span></div></div>" +
      cards.map(function (c) {
        return '<div class="pp-card pp-card--' + c[3] + '">' +
          '<span class="pp-card-icon">' + icon(c[2]) + "</span>" +
          '<div class="pp-card-body"><span class="pp-card-value">' + esc(c[1]) + "</span>" +
          '<span class="pp-card-label">' + esc(c[0]) + "</span></div></div>";
      }).join("") + "</div>";
  }

  function milestoneStatus(m, total) {
    if (m.state === "closed") return ["done", "Concluída"];
    if (m.due_on && new Date(m.due_on).getTime() < Date.now()) return ["late", "Atrasada"];
    if (!total) return ["planned", "Planejada"];
    if (!m.open_issues) return ["ready", "Issues concluídas"];
    return ["open", "Em andamento"];
  }

  function renderMilestones(milestones) {
    if (!milestones.length) return '<p class="pp-muted">Nenhuma milestone cadastrada.</p>';
    return '<div class="pp-milestones">' + milestones.map(function (m) {
      var total = m.open_issues + m.closed_issues;
      var pct = total ? Math.round((m.closed_issues / total) * 100) : 0;
      var status = milestoneStatus(m, total);
      var due = m.due_on
        ? '<span>Prazo ' + esc(fmtDate(m.due_on)) + " (" + timeTag(m.due_on) + ")</span>"
        : "";
      var desc = m.description
        ? '<p class="pp-milestone-desc" title="' + esc(m.description) + '">' + esc(m.description) + "</p>"
        : "";
      return '<article class="pp-milestone pp-milestone--' + status[0] + '">' +
        '<div class="pp-milestone-head"><a href="' + esc(m.html_url) + '">' + esc(m.title) + "</a>" +
        '<span class="pp-status pp-status--' + status[0] + '">' + status[1] + "</span></div>" +
        desc +
        '<div class="pp-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct +
        '" aria-label="Progresso de ' + esc(m.title) + '"><div class="pp-bar-fill" style="width:' + pct +
        '%"></div></div>' +
        '<div class="pp-milestone-meta"><span><strong>' + m.closed_issues + "/" + total + "</strong> issues · " +
        pct + "%</span>" + due + "</div></article>";
    }).join("") + "</div>";
  }

  function renderIssueTable(issues, opts) {
    if (!issues.length) return '<div class="pp-empty">' + esc(opts.empty) + "</div>";
    var rows = issues.map(function (i) {
      return "<tr>" +
        '<td class="pp-col-num" data-label="#"><a href="' + esc(i.html_url) + '">#' + esc(i.number) + "</a></td>" +
        '<td class="pp-col-title" data-label="Título"><a class="pp-issue-link" href="' + esc(i.html_url) + '">' +
        esc(i.title) + "</a>" + labelChips(i.labels) + "</td>" +
        '<td class="pp-col-ms" data-label="Milestone">' +
        (i.milestone ? esc(i.milestone.title) : '<span class="pp-muted">—</span>') + "</td>" +
        '<td data-label="Responsáveis">' + assignees(i.assignees) + "</td>" +
        '<td class="pp-col-date" data-label="' + esc(opts.dateLabel) + '">' + timeTag(i[opts.dateField]) + "</td>" +
        "</tr>";
    }).join("");
    return '<div class="pp-table-wrap"><table class="pp-table"><thead><tr>' +
      '<th class="pp-col-num">#</th><th>Título</th><th>Milestone</th><th>Responsáveis</th>' +
      '<th class="pp-col-date">' + esc(opts.dateLabel) + "</th>" +
      "</tr></thead><tbody>" + rows + "</tbody></table></div>";
  }

  function renderSkeleton(root) {
    var block = function (cls, n) {
      return new Array(n + 1).join('<div class="pp-skel ' + cls + '"></div>');
    };
    root.innerHTML = '<div class="pp-skeleton" aria-busy="true" aria-label="Carregando dados do GitHub">' +
      '<div class="pp-skel pp-skel--bar"></div>' +
      '<div class="pp-cards">' + block("pp-skel--card", 5) + "</div>" +
      '<div class="pp-milestones">' + block("pp-skel--milestone", 4) + "</div></div>";
  }

  function render(root, data) {
    var issues = data.items.filter(function (i) { return !i.pull_request; });
    var prs = data.items.filter(function (i) { return i.pull_request; });
    var openIssues = issues.filter(function (i) { return i.state === "open"; });
    var recentClosed = issues.filter(function (i) { return i.state === "closed"; })
      .sort(function (a, b) { return new Date(b.closed_at) - new Date(a.closed_at); })
      .slice(0, RECENT_CLOSED);

    root.innerHTML =
      renderToolbar(data) +
      renderCards(issues, prs) +
      sectionTitle("Milestones", data.milestones.length) + renderMilestones(data.milestones) +
      sectionTitle("Issues abertas", openIssues.length) +
      renderIssueTable(openIssues, { empty: "Nenhuma issue aberta. 🎉", dateField: "updated_at", dateLabel: "Atualizada" }) +
      sectionTitle("Concluídas recentemente", recentClosed.length) +
      renderIssueTable(recentClosed, { empty: "Nenhuma issue fechada ainda.", dateField: "closed_at", dateLabel: "Fechada" });

    root.querySelector(".pp-refresh").addEventListener("click", function () {
      try { sessionStorage.removeItem(CACHE_KEY); } catch (e) { /* ignore */ }
      refresh(root);
    });
  }

  function showError(root, err) {
    var old = root.querySelector(".pp-error");
    if (old) old.remove();
    if (root.querySelector(".pp-skeleton")) root.innerHTML = "";
    var box = document.createElement("div");
    box.className = "admonition warning pp-error";
    box.setAttribute("role", "alert");
    box.innerHTML = '<p class="admonition-title">Não foi possível carregar os dados do GitHub</p><p>' +
      esc(err.message) + ' — consulte diretamente as <a href="' + REPO_URL +
      '/issues">issues</a> e <a href="' + REPO_URL + '/milestones">milestones</a>.</p>';
    root.prepend(box);
  }

  async function refresh(root) {
    if (root.dataset.ppBusy) return;
    root.dataset.ppBusy = "1";
    root.classList.add("pp-loading");
    var btn = root.querySelector(".pp-refresh");
    if (btn) btn.disabled = true;
    try {
      render(root, await loadData());
    } catch (err) {
      showError(root, err);
    } finally {
      delete root.dataset.ppBusy;
      root.classList.remove("pp-loading");
      var current = root.querySelector(".pp-refresh");
      if (current) current.disabled = false;
    }
  }

  function init() {
    var root = document.getElementById("painel-projeto");
    if (!root || root.dataset.ppInit) return;
    root.dataset.ppInit = "1";
    root.setAttribute("aria-live", "polite");
    renderSkeleton(root);
    refresh(root);
    setInterval(function () {
      if (!document.hidden) refresh(root);
    }, REFRESH_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
