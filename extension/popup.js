const STAGE_URL = "http://localhost:5050/stage";

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

function setStatus(msg, isErr = false) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = "status" + (isErr ? " err" : "");
}

document.addEventListener("DOMContentLoaded", async () => {
  const tab = await getActiveTab();
  const pageInfo = document.getElementById("page-info");
  const saveBtn = document.getElementById("save-btn");

  if (!tab?.url || tab.url.startsWith("chrome://") || tab.url.startsWith("edge://")) {
    pageInfo.textContent = "Can't save this page";
    saveBtn.disabled = true;
    return;
  }

  const title = tab.title || new URL(tab.url).hostname || "page";
  pageInfo.textContent = title;

  saveBtn.addEventListener("click", async () => {
    saveBtn.disabled = true;
    setStatus("Saving…");

    try {
      const content = `we read "${title}"`;
      const res = await fetch(STAGE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, url: tab.url })
      });
      const data = await res.json();

      if (data.ok) {
        const msg = data.staged
          ? `Saved! ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`
          : `Added to log. ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`;
        setStatus(msg);
      } else {
        setStatus(data.error || "Failed", true);
        saveBtn.disabled = false;
      }
    } catch (err) {
      setStatus(err.message || "Can't reach server", true);
      saveBtn.disabled = false;
    }
  });
});
