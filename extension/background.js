const DEFAULT_STAGE_URL = "http://localhost:5050/stage";
const DEFAULT_STATUS_URL = "http://localhost:5050/status";
const DEFAULT_HANDBACK_URL = "http://localhost:5050/handback";
const QUEUE_KEY = "stageQueue";

function asStatusUrl(stageUrl) {
  try {
    const u = new URL(stageUrl);
    u.pathname = "/status";
    u.search = "";
    return u.toString();
  } catch {
    return DEFAULT_STATUS_URL;
  }
}

function asHandbackUrl(stageUrl) {
  try {
    const u = new URL(stageUrl || DEFAULT_STAGE_URL);
    u.pathname = "/handback";
    u.search = "";
    return u.toString();
  } catch {
    return DEFAULT_HANDBACK_URL;
  }
}

async function getConfig() {
  const stored = await chrome.storage.local.get({
    stageUrl: DEFAULT_STAGE_URL,
    apiKey: "",
    userId: "",
    queueRetryMinutes: 5
  });
  return {
    stageUrl: stored.stageUrl || DEFAULT_STAGE_URL,
    statusUrl: asStatusUrl(stored.stageUrl || DEFAULT_STAGE_URL),
    apiKey: (stored.apiKey || "").trim(),
    userId: (stored.userId || "").trim(),
    queueRetryMinutes: Math.max(1, Number(stored.queueRetryMinutes || 5))
  };
}

async function getQueue() {
  const data = await chrome.storage.local.get({ [QUEUE_KEY]: [] });
  return Array.isArray(data[QUEUE_KEY]) ? data[QUEUE_KEY] : [];
}

async function setQueue(queue) {
  await chrome.storage.local.set({ [QUEUE_KEY]: queue });
}

async function enqueueStage(payload, reason = "network") {
  const queue = await getQueue();
  queue.push({
    ts: new Date().toISOString(),
    reason,
    payload
  });
  await setQueue(queue);
  return queue.length;
}

function buildHeaders(cfg) {
  const headers = { "Content-Type": "application/json" };
  if (cfg.apiKey) headers["X-Api-Key"] = cfg.apiKey;
  return headers;
}

async function postStage(payload, cfg) {
  const res = await fetch(cfg.stageUrl, {
    method: "POST",
    headers: buildHeaders(cfg),
    body: JSON.stringify(payload)
  });
  const data = await res.json().catch(() => ({ ok: false, error: "Invalid JSON response" }));
  if (!res.ok || !data.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

async function postHandback(content, cfg) {
  const url = asHandbackUrl(cfg.stageUrl);
  const res = await fetch(url, {
    method: "POST",
    headers: buildHeaders(cfg),
    body: JSON.stringify({ content })
  });
  const data = await res.json().catch(() => ({ ok: false, error: "Invalid JSON response" }));
  if (!res.ok || !data.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

async function fetchStatus(cfg) {
  const url = new URL(cfg.statusUrl);
  if (cfg.userId) url.searchParams.set("user_id", cfg.userId);
  const res = await fetch(url.toString(), {
    method: "GET",
    headers: buildHeaders(cfg)
  });
  const data = await res.json().catch(() => ({ ok: false, error: "Invalid JSON response" }));
  if (!res.ok || !data.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

async function flushQueue() {
  const cfg = await getConfig();
  const queue = await getQueue();
  if (!queue.length) return { ok: true, flushed: 0, remaining: 0 };

  const remaining = [];
  let flushed = 0;
  for (const item of queue) {
    try {
      await postStage(item.payload, cfg);
      flushed += 1;
    } catch {
      remaining.push(item);
    }
  }
  await setQueue(remaining);
  return { ok: true, flushed, remaining: remaining.length };
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    stageUrl: DEFAULT_STAGE_URL,
    apiKey: "",
    userId: "",
    queueRetryMinutes: 5
  });
  chrome.contextMenus.create({
    id: "save-to-record",
    title: "Save to Record",
    contexts: ["page", "link", "selection"]
  });
  chrome.contextMenus.create({
    id: "save-transcript-to-record",
    title: "Save transcript to Record",
    contexts: ["selection"]
  });
  chrome.alarms.create("graceMarFlushQueue", { periodInMinutes: 5 });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "save-to-record") {
    const url = info.linkUrl || tab?.url || "";
    let title = info.linkText || tab?.title || "page";
    if (!title && url) {
      try {
        title = new URL(url).hostname || "page";
      } catch {
        title = "page";
      }
    }
    const selection = (info.selectionText || "").trim();
    const content = selection
      ? `we read "${title}". selected text: "${selection.slice(0, 500)}"`
      : `we read "${title}"`;
    await stageToRecord({ content, url, title, selection_text: selection || undefined });
  } else if (info.menuItemId === "save-transcript-to-record") {
    const selection = (info.selectionText || "").trim();
    if (selection) {
      await handbackToRecord({ content: selection });
    }
  }
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (!msg || typeof msg !== "object") return;
  if (msg.type === "stage") {
    stageToRecord(msg.payload || {})
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err?.message || "stage failed" }));
    return true;
  }
  if (msg.type === "handback") {
    handbackToRecord(msg.payload || {})
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err?.message || "handback failed" }));
    return true;
  }
  if (msg.type === "flushQueue") {
    flushQueue()
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err?.message || "flush failed" }));
    return true;
  }
  if (msg.type === "getStatus") {
    getConfig()
      .then((cfg) => fetchStatus(cfg))
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err?.message || "status failed" }));
    return true;
  }
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "graceMarFlushQueue") {
    flushQueue().catch(() => {});
  }
});

async function stageToRecord(payload) {
  const cfg = await getConfig();
  try {
    const body = {
      ...payload,
      user_id: cfg.userId || undefined
    };
    const data = await postStage(body, cfg);
    if (data.ok) {
      const msg = data.staged
        ? `Saved! ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`
        : `Added to log. ${data.pending_count} item${data.pending_count !== 1 ? "s" : ""} to review`;
      chrome.notifications?.create({
        type: "basic",
        title: "Grace-Mar",
        message: msg
      }).catch(() => {});
      return { ...data, queued: false };
    } else {
      throw new Error(data.error || "Request failed");
    }
  } catch (err) {
    const queuedCount = await enqueueStage(payload, err?.message || "network");
    chrome.notifications?.create({
        type: "basic",
        title: "Grace-Mar",
        message:
          (err?.message || "Could not reach server") +
          `. Queued offline (${queuedCount}).`
    }).catch(() => {});
    return { ok: true, queued: true, queue_count: queuedCount, error: err?.message || "failed" };
  }
}

async function handbackToRecord(payload) {
  const content = (payload.content || "").trim();
  if (!content) {
    throw new Error("Transcript content is empty");
  }
  const cfg = await getConfig();
  const data = await postHandback(content, cfg);
  if (data.ok) {
    const msg = data.staged
      ? "Transcript saved! Review in recursion-gate."
      : "Transcript added. Review in recursion-gate.";
    chrome.notifications?.create({
      type: "basic",
      title: "Grace-Mar",
      message: msg
    }).catch(() => {});
    return { ...data, queued: false };
  } else {
    throw new Error(data.error || "Request failed");
  }
}
