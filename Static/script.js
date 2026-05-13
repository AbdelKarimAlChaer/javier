const input = document.getElementById("thoughtInput");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const logOutput = document.getElementById("logOutput");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

// Update char count on input
input.addEventListener("input", () => {
  charCount.textContent = input.value.length;
});

// Submit on Ctrl+Enter
input.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter") submitThought();
});

function setStatus(state) {
  statusDot.className = "status-dot " + state;
  const labels = { "": "READY", loading: "PROCESSING", error: "ERROR" };
  statusText.textContent = labels[state] || "READY";
}

function addLog(message, type = "system") {
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.textContent = `_ ${message}`;
  logOutput.appendChild(entry);
  logOutput.scrollTop = logOutput.scrollHeight;
}

async function submitThought() {
  const thought = input.value.trim();
  if (!thought) return;

  // UI: loading state
  submitBtn.disabled = true;
  btnText.textContent = "PROCESSING...";
  setStatus("loading");
  addLog(`input received [${thought.length} chars]`, "processing");

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: thought }),
    });

    const data = await response.json();

    if (data.status === "ok") {
      addLog("note structured and saved", "success");
      input.value = "";
      charCount.textContent = "0";
      setStatus("");
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