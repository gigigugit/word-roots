/* =========================================================
   Word Roots Generator — frontend logic
   ========================================================= */

"use strict";

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
const state = {
  analysisResult: null,   // last /api/analyze response
  selectedPrefix: null,
  selectedRoot:   null,
  selectedSuffix: null,
  createdWord:    null,   // last /api/create response
  savedWordId:    null,   // id returned by /api/save
  allPrefixes:    {},
  allSuffixes:    {},
  allRoots:       {},
};

// ---------------------------------------------------------------------------
// Utility helpers
// ---------------------------------------------------------------------------
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const id = `toast-${Date.now()}`;
  const bg = type === "success" ? "bg-success" : type === "error" ? "bg-danger" : "bg-primary";
  container.insertAdjacentHTML(
    "beforeend",
    `<div id="${id}" class="toast custom-toast text-white ${bg} border-0 show mb-2" role="alert">
       <div class="d-flex">
         <div class="toast-body">${message}</div>
         <button type="button" class="btn-close btn-close-white me-2 m-auto"
                 data-bs-dismiss="toast"></button>
       </div>
     </div>`
  );
  setTimeout(() => document.getElementById(id)?.remove(), 3500);
}

function show(id)  { document.getElementById(id).classList.remove("d-none"); }
function hide(id)  { document.getElementById(id).classList.add("d-none"); }
function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

async function apiFetch(url, options = {}) {
  const defaults = { headers: { "Content-Type": "application/json" } };
  const res = await fetch(url, { ...defaults, ...options });
  const json = await res.json();
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

// ---------------------------------------------------------------------------
// Boot: load linguistic data
// ---------------------------------------------------------------------------
async function loadLinguisticData() {
  const [prefixes, suffixes, roots] = await Promise.all([
    apiFetch("/api/prefixes"),
    apiFetch("/api/suffixes"),
    apiFetch("/api/roots"),
  ]);
  state.allPrefixes = prefixes;
  state.allSuffixes = suffixes;
  state.allRoots    = roots;
  renderSelectors();
}

// ---------------------------------------------------------------------------
// Step 1 — Analyse a word
// ---------------------------------------------------------------------------
document.getElementById("btn-analyze").addEventListener("click", analyzeWord);
document.getElementById("input-word").addEventListener("keydown", (e) => {
  if (e.key === "Enter") analyzeWord();
});

async function analyzeWord() {
  const word = document.getElementById("input-word").value.trim();
  if (!word) return showToast("Please enter a word first.", "error");

  try {
    const result = await apiFetch("/api/analyze", {
      method: "POST",
      body: JSON.stringify({ word }),
    });
    state.analysisResult = result;
    renderAnalysis(result);
    show("analysis-results");
    // Pre-select identified components
    if (result.prefix) selectPill("prefix", result.prefix);
    if (result.root)   selectRootPill(result.root);
    if (result.suffix) selectPill("suffix", result.suffix);
  } catch (err) {
    showToast(err.message, "error");
  }
}

function renderAnalysis(r) {
  // Visual breakdown
  const bd = document.getElementById("word-breakdown");
  bd.innerHTML = "";

  const parts = [
    { key: r.prefix, type: "prefix", info: r.prefix_info },
    { key: r.root,   type: "root",   info: r.root_info   },
    { key: r.suffix, type: "suffix", info: r.suffix_info },
  ].filter((p) => p.key);

  parts.forEach((p) => {
    const cls = p.info ? p.type : "unknown";
    const display = p.info
      ? (p.info.display || p.key)
      : p.key;
    const label =
      p.type === "prefix" ? "Prefix" :
      p.type === "suffix" ? "Suffix" : "Root";
    bd.insertAdjacentHTML(
      "beforeend",
      `<div class="word-part ${cls}">
         ${display}
         <span class="word-part-label">${label}</span>
       </div>`
    );
  });

  // Component info cards
  renderComponentCard("prefix-info-card", r.prefix_info, r.prefix, "prefix");
  renderComponentCard("root-info-card",   r.root_info,   r.root,   "root");
  renderComponentCard("suffix-info-card", r.suffix_info, r.suffix, "suffix");

  const dbNote = document.getElementById("root-db-note");
  dbNote.textContent = r.root_in_database
    ? `✓ Root '${r.root}' found in database.`
    : `Root '${r.root}' was identified but is not in our database — you can still use it to build new words.`;
  dbNote.className = r.root_in_database ? "text-success small" : "text-warning small";
}

function renderComponentCard(cardId, info, key, type) {
  const card = document.getElementById(cardId);
  if (!card) return;
  if (!key) { card.style.display = "none"; return; }
  card.style.display = "";
  card.innerHTML = `
    <div class="label">${type}</div>
    <div class="display-text">${info ? info.display : key}</div>
    ${info ? `<div class="meaning">${info.meaning}</div>
    <div class="small text-muted mt-1">Origin: ${info.origin}</div>
    <div class="small text-muted">Examples: ${(info.examples || []).join(", ")}</div>` : ""}
  `;
}

// ---------------------------------------------------------------------------
// Step 2 — Word builder (selectors)
// ---------------------------------------------------------------------------
function renderSelectors() {
  renderPillGroup("prefix-selector", state.allPrefixes, "prefix", "prefix-pill");
  renderPillGroup("suffix-selector", state.allSuffixes, "suffix", "suffix-pill");
  renderRootPills();
}

function renderPillGroup(containerId, data, type, pillClass) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  Object.entries(data)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([key, info]) => {
      const btn = document.createElement("span");
      btn.className = `selector-pill ${pillClass}`;
      btn.dataset.key = key;
      btn.title = info.meaning;
      btn.textContent = info.display;
      btn.addEventListener("click", () => {
        if (type === "prefix") togglePill("prefix", key, btn);
        else                   togglePill("suffix", key, btn);
      });
      container.appendChild(btn);
    });
}

function renderRootPills() {
  const container = document.getElementById("root-selector");
  container.innerHTML = "";

  // Custom root input
  const customDiv = document.createElement("div");
  customDiv.className = "d-flex gap-2 mb-2 flex-wrap align-items-center";
  customDiv.innerHTML = `
    <input id="custom-root-input" type="text" class="form-control form-control-sm"
           style="max-width:160px" placeholder="Type a root…">
    <button id="btn-use-custom-root" class="btn btn-sm btn-outline-primary">Use</button>
  `;
  container.appendChild(customDiv);

  document.getElementById("btn-use-custom-root").addEventListener("click", () => {
    const val = document.getElementById("custom-root-input").value.trim().toLowerCase();
    if (val) selectRootPill(val);
  });
  document.getElementById("custom-root-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") document.getElementById("btn-use-custom-root").click();
  });

  // Known root pills
  const pillRow = document.createElement("div");
  Object.entries(state.allRoots)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([key, info]) => {
      const btn = document.createElement("span");
      btn.className = "selector-pill root-pill";
      btn.dataset.key = key;
      btn.title = info.meaning;
      btn.textContent = info.display;
      btn.addEventListener("click", () => selectRootPill(key));
      pillRow.appendChild(btn);
    });
  container.appendChild(pillRow);
}

function togglePill(type, key, btnEl) {
  const isPrefix = type === "prefix";
  const current  = isPrefix ? state.selectedPrefix : state.selectedSuffix;
  const selector = isPrefix ? ".prefix-pill" : ".suffix-pill";

  // Deselect current
  document.querySelectorAll(selector).forEach((p) => p.classList.remove("selected"));

  if (current === key) {
    // toggling off
    if (isPrefix) state.selectedPrefix = null;
    else          state.selectedSuffix = null;
  } else {
    if (isPrefix) state.selectedPrefix = key;
    else          state.selectedSuffix = key;
    btnEl.classList.add("selected");
  }
  updatePreview();
}

function selectPill(type, key) {
  const isPrefix = type === "prefix";
  const selector = isPrefix ? `.prefix-pill[data-key="${key}"]` : `.suffix-pill[data-key="${key}"]`;
  const btn = document.querySelector(selector);
  if (btn) { btn.classList.add("selected"); }
  if (isPrefix) state.selectedPrefix = key;
  else          state.selectedSuffix = key;
}

function selectRootPill(key) {
  document.querySelectorAll(".root-pill").forEach((p) => p.classList.remove("selected"));
  const btn = document.querySelector(`.root-pill[data-key="${key}"]`);
  if (btn) btn.classList.add("selected");
  state.selectedRoot = key;
  // Keep custom input in sync
  const inp = document.getElementById("custom-root-input");
  if (inp) inp.value = key;
  updatePreview();
}

// ---------------------------------------------------------------------------
// Live preview
// ---------------------------------------------------------------------------
function updatePreview() {
  const { selectedPrefix: p, selectedRoot: r, selectedSuffix: s } = state;

  if (!r) {
    document.getElementById("word-preview").textContent = "—";
    document.getElementById("preview-breakdown").innerHTML = "";
    hide("preview-actions");
    return;
  }

  const word = (p || "") + r + (s || "");
  document.getElementById("word-preview").textContent = word;

  // Mini breakdown
  const bd = document.getElementById("preview-breakdown");
  bd.innerHTML = "";
  if (p) bd.insertAdjacentHTML("beforeend",
    `<span class="badge me-1" style="background:var(--prefix-color)">${state.allPrefixes[p]?.display || p}</span>`);
  bd.insertAdjacentHTML("beforeend",
    `<span class="badge me-1" style="background:var(--root-color)">${r}</span>`);
  if (s) bd.insertAdjacentHTML("beforeend",
    `<span class="badge" style="background:var(--suffix-color)">${state.allSuffixes[s]?.display || s}</span>`);

  show("preview-actions");
}

// ---------------------------------------------------------------------------
// Step 3 — Create / Save / Export / Share / Feedback
// ---------------------------------------------------------------------------
document.getElementById("btn-create").addEventListener("click", async () => {
  const { selectedPrefix: prefix, selectedRoot: root, selectedSuffix: suffix } = state;
  if (!root) return showToast("Please select or type a root first.", "error");

  try {
    const result = await apiFetch("/api/create", {
      method: "POST",
      body: JSON.stringify({ prefix, root, suffix }),
    });
    state.createdWord = result;
    state.savedWordId = null;
    renderCreatedWord(result);
    show("created-word-section");
    document.getElementById("created-word-section").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    showToast(err.message, "error");
  }
});

function renderCreatedWord(r) {
  setText("created-word-display", r.word);
  setText("created-definition",  r.definition);
  setText("created-example",     r.example);

  // Component badges
  const badges = document.getElementById("created-badges");
  badges.innerHTML = "";
  if (r.prefix) badges.insertAdjacentHTML("beforeend",
    `<span class="badge me-1" style="background:var(--prefix-color)">prefix: ${r.prefix_info?.display || r.prefix}</span>`);
  badges.insertAdjacentHTML("beforeend",
    `<span class="badge me-1" style="background:var(--root-color)">root: ${r.root_info?.display || r.root}</span>`);
  if (r.suffix) badges.insertAdjacentHTML("beforeend",
    `<span class="badge" style="background:var(--suffix-color)">suffix: ${r.suffix_info?.display || r.suffix}</span>`);

  hide("save-success-msg");
  document.getElementById("btn-save").disabled = false;
}

document.getElementById("btn-save").addEventListener("click", async () => {
  if (!state.createdWord) return;
  const { word, prefix, root, suffix, definition, example } = state.createdWord;
  try {
    const res = await apiFetch("/api/save", {
      method: "POST",
      body: JSON.stringify({ word, prefix, root, suffix, definition, example }),
    });
    state.savedWordId = res.id;
    showToast("Word saved!", "success");
    show("save-success-msg");
    document.getElementById("btn-save").disabled = true;
    loadSavedWords();
  } catch (err) {
    showToast(err.message, "error");
  }
});

document.getElementById("btn-export").addEventListener("click", () => {
  if (!state.savedWordId) return showToast("Save the word first.", "error");
  window.location.href = `/api/export/${state.savedWordId}`;
});

document.getElementById("btn-copy-share").addEventListener("click", async () => {
  if (!state.savedWordId) return showToast("Save the word first.", "error");
  try {
    const data = await apiFetch(`/api/share/${state.savedWordId}`);
    await navigator.clipboard.writeText(data.share_text);
    showToast("Share text copied to clipboard!", "success");
  } catch {
    showToast("Could not copy — try saving first.", "error");
  }
});

document.getElementById("btn-tweet").addEventListener("click", async () => {
  if (!state.savedWordId) return showToast("Save the word first.", "error");
  try {
    const data = await apiFetch(`/api/share/${state.savedWordId}`);
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(data.share_text)}`;
    window.open(url, "_blank");
  } catch {
    showToast("Could not prepare tweet.", "error");
  }
});

// ---------------------------------------------------------------------------
// Saved words + feedback
// ---------------------------------------------------------------------------
async function loadSavedWords() {
  try {
    const words = await apiFetch("/api/words");
    renderSavedWords(words);
    if (words.length > 0) show("saved-section");
  } catch {/* ignore */}
}

function renderSavedWords(words) {
  const list = document.getElementById("saved-words-list");
  list.innerHTML = "";

  if (words.length === 0) {
    list.innerHTML = '<p class="text-muted">No words saved yet.</p>';
    return;
  }

  words.forEach((w) => {
    const stars = renderStars(w.id, w.avg_rating);
    list.insertAdjacentHTML(
      "beforeend",
      `<div class="word-card" id="wc-${w.id}">
         <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
           <div>
             <span class="word-title">${w.word}</span>
             <span class="word-meta ms-2">${new Date(w.created_at).toLocaleDateString()}</span>
           </div>
           <div class="d-flex gap-1">
             <a href="/api/export/${w.id}" class="btn btn-sm btn-outline-secondary">Export</a>
             <button class="btn btn-sm btn-outline-primary"
                     onclick="shareWord(${w.id})">Share</button>
           </div>
         </div>
         <p class="mb-1 mt-2 small text-muted">${w.definition || ""}</p>
         <p class="mb-2 small fst-italic">${w.example || ""}</p>
         <div class="d-flex align-items-center gap-3 flex-wrap">
           <div>${stars}</div>
           <span class="text-muted small">${w.feedback_count} rating${w.feedback_count !== 1 ? "s" : ""}</span>
         </div>
         <div id="feedback-form-${w.id}" class="mt-2 d-none">
           <textarea class="form-control form-control-sm mb-1" rows="2"
                     id="comment-${w.id}" placeholder="Optional comment…"></textarea>
           <button class="btn btn-sm btn-primary" onclick="submitFeedback(${w.id})">Submit</button>
         </div>
       </div>`
    );
  });
}

function renderStars(wordId, avgRating) {
  let html = '<span class="me-1 small text-muted">Rate:</span>';
  for (let i = 1; i <= 5; i++) {
    const active = i <= Math.round(avgRating) ? "active" : "";
    html += `<button class="star-btn ${active}" onclick="rateWord(${wordId}, ${i})">★</button>`;
  }
  return html;
}

window.rateWord = function (wordId, rating) {
  // Show feedback form
  const form = document.getElementById(`feedback-form-${wordId}`);
  if (form) {
    form.classList.remove("d-none");
    form.dataset.rating = rating;
    // Highlight stars
    const card = document.getElementById(`wc-${wordId}`);
    card.querySelectorAll(".star-btn").forEach((btn, idx) => {
      btn.classList.toggle("active", idx < rating);
    });
  }
};

window.submitFeedback = async function (wordId) {
  const form    = document.getElementById(`feedback-form-${wordId}`);
  const rating  = parseInt(form.dataset.rating || "0", 10);
  const comment = (document.getElementById(`comment-${wordId}`)?.value || "").trim();

  if (!rating) return showToast("Please click a star first.", "error");
  try {
    await apiFetch("/api/feedback", {
      method: "POST",
      body: JSON.stringify({ word_id: wordId, rating, comment }),
    });
    showToast("Thank you for your feedback!", "success");
    form.classList.add("d-none");
    loadSavedWords();
  } catch (err) {
    showToast(err.message, "error");
  }
};

window.shareWord = async function (wordId) {
  try {
    const data = await apiFetch(`/api/share/${wordId}`);
    await navigator.clipboard.writeText(data.share_text);
    showToast("Share text copied!", "success");
  } catch {
    showToast("Clipboard not available.", "error");
  }
};

// ---------------------------------------------------------------------------
// Initialise
// ---------------------------------------------------------------------------
(async () => {
  await loadLinguisticData();
  await loadSavedWords();
})();
