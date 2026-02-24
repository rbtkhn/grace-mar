const DEFAULT_STAGE_URL = "http://localhost:5050/stage";

function setStatus(msg, isErr = false) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = isErr ? "err" : "";
}

function asStatusUrl(stageUrl) {
  try {
    const u = new URL(stageUrl || DEFAULT_STAGE_URL);
    u.pathname = "/status";
    u.search = "";
    return u.toString();
  } catch {
    return "http://localhost:5050/status";
  }
}

async function loadSettings() {
  const cfg = await chrome.storage.local.get({
    stageUrl: DEFAULT_STAGE_URL,
    apiKey: "",
    userId: "",
    queueRetryMinutes: 5
  });
  document.getElementById("stageUrl").value = cfg.stageUrl || DEFAULT_STAGE_URL;
  document.getElementById("apiKey").value = cfg.apiKey || "";
  document.getElementById("userId").value = cfg.userId || "";
  document.getElementById("queueRetryMinutes").value = Number(cfg.queueRetryMinutes || 5);
}

async function saveSettings() {
  const stageUrl = (document.getElementById("stageUrl").value || DEFAULT_STAGE_URL).trim();
  const apiKey = (document.getElementById("apiKey").value || "").trim();
  const userId = (document.getElementById("userId").value || "").trim();
  const queueRetryMinutes = Math.max(1, Number(document.getElementById("queueRetryMinutes").value || 5));

  await chrome.storage.local.set({ stageUrl, apiKey, userId, queueRetryMinutes });
  chrome.alarms.create("graceMarFlushQueue", { periodInMinutes: queueRetryMinutes });
  setStatus("Settings saved.");
}

async function testStatus() {
  const cfg = await chrome.storage.local.get({ stageUrl: DEFAULT_STAGE_URL, apiKey: "", userId: "" });
  const url = new URL(asStatusUrl(cfg.stageUrl));
  if (cfg.userId) url.searchParams.set("user_id", cfg.userId);
  const headers = {};
  if (cfg.apiKey) headers["X-Api-Key"] = cfg.apiKey;
  try {
    const res = await fetch(url.toString(), { method: "GET", headers });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      setStatus(`Status test failed: ${data.error || `HTTP ${res.status}`}`, true);
      return;
    }
    setStatus(`Status ok — pending: ${data.pending_count ?? "?"}`);
  } catch (err) {
    setStatus(`Status test failed: ${err.message || "network error"}`, true);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadSettings();
  document.getElementById("saveBtn").addEventListener("click", saveSettings);
  document.getElementById("testBtn").addEventListener("click", testStatus);
});
