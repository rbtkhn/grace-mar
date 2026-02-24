const STAGE_URL = "http://localhost:5050/stage";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "save-to-record",
    title: "Save to Record",
    contexts: ["page", "link"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "save-to-record") {
    const url = info.linkUrl || tab?.url || "";
    const title = info.linkText || tab?.title || new URL(url).hostname || "page";
    const content = `we read "${title}"`;
    await stageToRecord(content, url);
  }
});

async function stageToRecord(content, url = "") {
  try {
    const body = url ? { content, url } : { content };
    const res = await fetch(STAGE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.ok) {
      const msg = data.staged
        ? `Saved! ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`
        : `Added to log. ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`;
      chrome.notifications?.create({
        type: "basic",
        title: "Grace-Mar",
        message: msg
      }).catch(() => {});
    } else {
      throw new Error(data.error || "Request failed");
    }
  } catch (err) {
    chrome.notifications?.create({
        type: "basic",
        title: "Grace-Mar",
        message: err.message || "Could not reach local server. Run: python scripts/handback_server.py"
    }).catch(() => {});
  }
}
