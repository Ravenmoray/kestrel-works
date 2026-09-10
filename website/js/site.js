// Kestrel Works — shared site helpers: a tiny markdown renderer (no
// external dependencies, so the site works fully offline) and the update
// feed loader/renderer used on index.html and updates.html.

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function inline(s) {
  s = escapeHtml(s);
  s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return s;
}

// Minimal markdown -> HTML: headers, hr, unordered lists, paragraphs.
// Built for our own controlled content (HISTORY.md / CHARTER.md), not
// arbitrary markdown.
function mdToHtml(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  let html = "";
  let inList = false;
  let inCode = false;

  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };

  for (const raw of lines) {
    const line = raw;

    if (line.trim().startsWith("```")) {
      inCode = !inCode;
      html += inCode ? "<pre><code>" : "</code></pre>";
      continue;
    }
    if (inCode) { html += escapeHtml(line) + "\n"; continue; }

    if (/^---+\s*$/.test(line)) { closeList(); html += "<hr>"; continue; }
    if (/^\s*$/.test(line)) { closeList(); continue; }

    const h = line.match(/^(#{1,3})\s+(.*)$/);
    if (h) {
      closeList();
      const level = h[1].length;
      html += `<h${level}>${inline(h[2])}</h${level}>`;
      continue;
    }

    const li = line.match(/^\s*[-*]\s+(.*)$/);
    if (li) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${inline(li[1])}</li>`;
      continue;
    }

    closeList();
    html += `<p>${inline(line)}</p>`;
  }
  closeList();
  return html;
}

async function loadUpdates() {
  const res = await fetch("data/updates.json");
  if (!res.ok) throw new Error("could not load updates.json");
  const updates = await res.json();
  return updates.slice().sort((a, b) => (a.date < b.date ? 1 : -1));
}

function updateCardHtml(u) {
  const link = u.link
    ? `<div><a href="${escapeHtml(u.link)}">${u.link.startsWith("http") ? "View on GitHub →" : "View the file →"}</a></div>`
    : "";
  return `
    <article class="card">
      <div class="meta"><span class="dept">${escapeHtml(u.department)}</span> · ${escapeHtml(u.date)}</div>
      <h3>${escapeHtml(u.title)}</h3>
      <p>${escapeHtml(u.summary)}</p>
      ${link}
    </article>`;
}

async function renderUpdatesInto(elId, limit) {
  const el = document.getElementById(elId);
  if (!el) return;
  try {
    const updates = await loadUpdates();
    const shown = limit ? updates.slice(0, limit) : updates;
    if (shown.length === 0) {
      el.innerHTML = '<p class="empty">No updates logged yet.</p>';
      return;
    }
    el.innerHTML = shown.map(updateCardHtml).join("\n");
  } catch (e) {
    el.innerHTML = '<p class="empty">Updates feed unavailable right now.</p>';
  }
}

async function renderYearProgress(elId, path) {
  const el = document.getElementById(elId);
  if (!el) return;
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error("fetch failed");
    const s = await res.json();
    const pct = Math.min(100, Math.round((s.simulated_day / s.year_length_days) * 1000) / 10);
    const statusLabel = { running: "Running", completed: "Complete", stopped: "Stopped" }[s.status] || s.status;
    el.innerHTML = `
      <div class="card">
        <div class="meta">
          <span class="pill">${escapeHtml(statusLabel)}</span>
          &nbsp;Day ${s.simulated_day} of ${s.year_length_days} &middot; simulated date ${escapeHtml(s.simulated_date)}
        </div>
        <div style="background:var(--line);border-radius:999px;height:10px;overflow:hidden;margin:10px 0;">
          <div style="background:var(--accent);height:100%;width:${pct}%;"></div>
        </div>
        <p style="margin:0;color:var(--ink-soft);font-size:0.9rem;">
          Last department to run: <strong>${escapeHtml(s.last_department || "—")}</strong>
          ${s.stopped_reason ? ` &middot; ${escapeHtml(s.stopped_reason)}` : ""}
        </p>
      </div>`;
  } catch (e) {
    el.innerHTML = '<p class="empty">Year One progress unavailable right now.</p>';
  }
}

async function renderMarkdownInto(elId, path) {
  const el = document.getElementById(elId);
  if (!el) return;
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error("fetch failed");
    const text = await res.text();
    el.innerHTML = mdToHtml(text);
    el.classList.add("markdown");
  } catch (e) {
    el.innerHTML = `<p class="empty">Could not load ${escapeHtml(path)} — is the site running via scripts/serve.sh?</p>`;
  }
}
