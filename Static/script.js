const input = document.getElementById("thoughtInput");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const logOutput = document.getElementById("logOutput");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

// ─── Init ────────────────────────────────────────────────────────────────────

input.addEventListener("input", () => {
  charCount.textContent = input.value.length;
});

input.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter") submitThought();
});

window.addEventListener("load", loadTags);

// ─── Status & Log ────────────────────────────────────────────────────────────

function setStatus(state) {
  statusDot.className = "status-dot " + state;
  const labels = {"": "READY", loading: "PROCESSING", error: "ERROR"};
  statusText.textContent = labels[state] || "READY";
}

function addLog(message, type = "system") {
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.textContent = `_ ${message}`;
  logOutput.appendChild(entry);
  logOutput.scrollTop = logOutput.scrollHeight;
}

// ─── Tabs ────────────────────────────────────────────────────────────────────

function showTab(tab) {
  document.getElementById("panelLog").classList.toggle("hidden", tab !== "log");
  document.getElementById("panelNote").classList.toggle("hidden", tab !== "note");
  document.getElementById("tabLog").classList.toggle("active", tab === "log");
  document.getElementById("tabNote").classList.toggle("active", tab === "note");
}

// ─── Tag Browser ─────────────────────────────────────────────────────────────

async function loadTags() {
  const res = await fetch("/tags");
  const data = await res.json();
  const tagList = document.getElementById("tagList");
  tagList.innerHTML = "";

  if (!data.tags || data.tags.length === 0) {
    tagList.innerHTML = '<div class="dim">no tags yet</div>';
    return;
  }

  data.tags.forEach(tag => {
    const el = document.createElement("div");
    el.className = "tag-item";
    el.textContent = `# ${tag}`;
    el.onclick = () => loadNotes(tag, el);
    tagList.appendChild(el);
  });
}

function filterTags() {
  const query = document.getElementById("tagSearch").value.toLowerCase();
  document.querySelectorAll(".tag-item").forEach(el => {
    el.classList.toggle("hidden", !el.textContent.toLowerCase().includes(query));
  });
}

async function loadNotes(tag, tagEl) {
  // Mark active tag
  document.querySelectorAll(".tag-item").forEach(t => t.classList.remove("active"));
  tagEl.classList.add("active");

  const res = await fetch(`/tags/${tag}`);
  const data = await res.json();

  document.getElementById("tagList").classList.add("hidden");
  document.getElementById("noteList").classList.remove("hidden");
  document.getElementById("activeTag").textContent = `# ${tag}`;

  const noteItems = document.getElementById("noteItems");
  noteItems.innerHTML = "";

  if (!data.notes || data.notes.length === 0) {
    noteItems.innerHTML = '<div class="dim">no notes</div>';
    return;
  }

  data.notes.forEach(note => {
    const el = document.createElement("div");
    el.className = "note-item";
    el.textContent = note.title || note.filename;
    el.onclick = () => openNote(note.filepath, note.filename);
    noteItems.appendChild(el);
  });
}

function clearNoteList() {
  document.getElementById("noteList").classList.add("hidden");
  document.getElementById("tagList").classList.remove("hidden");
  document.querySelectorAll(".tag-item").forEach(t => t.classList.remove("active"));
}

// ─── Note Viewer ─────────────────────────────────────────────────────────────

async function openNote(filepath, filename) {
  const res = await fetch(`/note?path=${encodeURIComponent(filepath)}`);
  const data = await res.json();

  document.getElementById("noteLabel").textContent = `// ${filename}`;
  document.getElementById("noteContent").innerHTML = marked.parse(data.content);
  showTab("note");
}

// ─── Submit ──────────────────────────────────────────────────────────────────

async function submitThought() {
  const thought = input.value.trim();
  if (!thought) return;

  submitBtn.disabled = true;
  btnText.textContent = "PROCESSING...";
  setStatus("loading");
  addLog(`input received [${thought.length} chars]`, "processing");

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({input: thought}),
    });

    const data = await response.json();

    if (data.status === "ok") {
      addLog("note structured and saved", "success");
      input.value = "";
      charCount.textContent = "0";
      setStatus("");
      loadTags(); // refresh tag browser
    } else {
      addLog(`error: ${data.message}`, "error");
      setStatus("error");
      setTimeout(() => setStatus(""), 3000);
    }
  } catch (err) {
    addLog("connection error – is the server running?", "error");
    setStatus("error");
    setTimeout(() => setStatus(""), 3000);
  } finally {
    submitBtn.disabled = false;
    btnText.textContent = "STRUCTURE →";
  }
}