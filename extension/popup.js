async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

function sendMessage(type, payload = {}) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage({ type, payload }, (resp) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      if (!resp) {
        reject(new Error("No response from extension service worker"));
        return;
      }
      if (!resp.ok) {
        reject(new Error(resp.error || "Request failed"));
        return;
      }
      resolve(resp.data);
    });
  });
}

function setStatus(msg, isErr = false) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = "status" + (isErr ? " err" : "");
}

function setPipelineMeta(msg) {
  const el = document.getElementById("pipeline-meta");
  el.textContent = msg;
}

async function extractSnippet(tabId) {
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId },
      func: () => {
        const selected = (window.getSelection && window.getSelection().toString().trim()) || "";
        if (selected) return selected.slice(0, 500);
        const p = document.querySelector("article p, main p, p");
        return (p?.innerText || "").trim().slice(0, 500);
      }
    });
    return (results?.[0]?.result || "").trim();
  } catch {
    return "";
  }
}

function summarizeStatus(data) {
  const pending = Number(data.pending_count || 0);
  const oldest = data.oldest_pending_days;
  const oldestText = oldest === null || oldest === undefined ? "n/a" : `${oldest}d`;
  return `Pending: ${pending} · Oldest: ${oldestText}`;
}

document.addEventListener("DOMContentLoaded", async () => {
  const tab = await getActiveTab();
  const pageInfo = document.getElementById("page-info");
  const saveBtn = document.getElementById("save-btn");
  const retryBtn = document.getElementById("retry-btn");
  const statusBtn = document.getElementById("status-btn");
  const settingsLink = document.getElementById("settings-link");

  if (!tab?.url || tab.url.startsWith("chrome://") || tab.url.startsWith("edge://")) {
    pageInfo.textContent = "Can't save this page";
    saveBtn.disabled = true;
    return;
  }

  const title = tab.title || new URL(tab.url).hostname || "page";
  pageInfo.textContent = title;

  settingsLink.addEventListener("click", (e) => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });

  async function refreshStatus() {
    try {
      const data = await sendMessage("getStatus");
      setPipelineMeta(summarizeStatus(data));
    } catch (err) {
      setPipelineMeta(`Status unavailable (${err.message || "error"})`);
    }
  }

  retryBtn.addEventListener("click", async () => {
    retryBtn.disabled = true;
    setStatus("Retrying queued captures…");
    try {
      const data = await sendMessage("flushQueue");
      setStatus(`Retried: ${data.flushed || 0} sent, ${data.remaining || 0} remaining`);
    } catch (err) {
      setStatus(err.message || "Retry failed", true);
    } finally {
      retryBtn.disabled = false;
      refreshStatus();
    }
  });

  statusBtn.addEventListener("click", async () => {
    statusBtn.disabled = true;
    await refreshStatus();
    statusBtn.disabled = false;
  });

  saveBtn.addEventListener("click", async () => {
    saveBtn.disabled = true;
    setStatus("Saving…");

    try {
      const snippet = await extractSnippet(tab.id);
      const content = snippet
        ? `we read "${title}". excerpt: "${snippet}"`
        : `we read "${title}"`;
      const data = await sendMessage("stage", {
        content,
        url: tab.url,
        title,
        selection_text: snippet || undefined
      });

      if (data.queued) {
        setStatus(`Server unavailable — queued offline (${data.queue_count || 0})`, true);
        saveBtn.disabled = false;
      } else {
        const msg = data.staged
          ? `Saved! ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`
          : `Added to log. ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`;
        setStatus(msg);
      }
    } catch (err) {
      setStatus(err.message || "Can't reach server", true);
      saveBtn.disabled = false;
    } finally {
      refreshStatus();
    }
  });

  const transcriptBtn = document.getElementById("transcript-btn");
  const transcriptInput = document.getElementById("transcript-input");
  transcriptBtn.addEventListener("click", async () => {
    const content = (transcriptInput.value || "").trim();
    if (!content) {
      setStatus("Paste transcript first", true);
      return;
    }
    transcriptBtn.disabled = true;
    setStatus("Saving transcript…");
    try {
      const data = await sendMessage("handback", { content });
      setStatus(data.staged ? "Transcript saved! Review in recursion-gate." : "Transcript added. Review in recursion-gate.");
      transcriptInput.value = "";
    } catch (err) {
      setStatus(err.message || "Can't reach server", true);
    } finally {
      transcriptBtn.disabled = false;
      refreshStatus();
    }
  });

  await refreshStatus();
});
