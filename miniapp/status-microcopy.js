(function(global) {
  var COPY = {
    chat: {
      waiting: [
        "Finding the thread...",
        "Getting ready to answer...",
        "Listening for the shape of it..."
      ]
    },
    grounded_record: {
      waiting: [
        "Checking the Record...",
        "Reading what is already documented...",
        "Grounding in Grace-Mar's Record..."
      ],
      error: "Could not check the Record right now."
    },
    gate_review: {
      staging: "Staging for review...",
      reviewing: "Reviewing pending changes...",
      applying: "Applying approved changes...",
      approvedLine: "approved — use the merge buttons above to write the Record.",
      emptyApprovedLine: "No approved items waiting merge.",
      error: "That review action did not work."
    },
    maintenance: {
      unlocking: "Checking operator access...",
      refreshing: "Refreshing this view..."
    }
  };

  function pick(value) {
    if (Array.isArray(value)) {
      if (!value.length) return "";
      return value[Math.floor(Math.random() * value.length)];
    }
    return value || "";
  }

  function phrase(lane, key, fallback) {
    var laneCopy = COPY[lane] || {};
    return pick(laneCopy[key]) || fallback || "";
  }

  global.GraceMarStatusMicrocopy = {
    phrase: phrase
  };
})(window);
