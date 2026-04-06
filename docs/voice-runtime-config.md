# Voice and avatar runtime config

Repo-root **`runtime_config.json`** (copy from **`runtime_config.example.json`**) may include a **`voice_avatar`** object. This document summarizes the nested contract, how it interacts with **`constitutional_critique`**, and how **`latency_mode`** adjusts critique thresholds for low-latency voice paths.

**Monitoring:** Use the root **`monitoring`** block only. Do **not** add a nested **`voice_avatar.monitoring`** object.

---

## Schema summary

| Field | Purpose |
|--------|---------|
| **`voice_avatar.enabled`** | Master switch for the **voice stack** (STT/TTS when wired). Default `false`. |
| **`voice_avatar.latency_mode`** | `"ultra_low"` \| `"balanced"` \| `"governed"`. Drives `merge_critique_for_latency_mode()` over **`constitutional_critique`** (see below). |
| **`voice_avatar.stt`** | Placeholders: `provider`, `model`, `language`, `streaming`. |
| **`voice_avatar.tts`** | Placeholders: `provider`, `voice_id`, `model`, `streaming`, `speed`, `stability`. |
| **`voice_avatar.avatar`** | Nested avatar: `enabled`, `type` (`live2d` \| `vrm` \| `none`), `model_path`, `renderer_url`, `emotion_mapping`. |
| **`voice_avatar.barge_in`** | Policy placeholder: `enabled`, `vad_sensitivity` (`low` \| `medium` \| `high`). |
| **`voice_avatar.cache`** | Future voice cache: `enabled`, `ttl_minutes`, `size`. Not the same as **`constitutional_critique.cache_ttl_seconds`**. |

**Legacy (deprecated):** Flat **`avatar_type`**, **`avatar_model_path`**, and **`renderer_url`** on **`voice_avatar`** are still read when **`avatar`** is **absent**. If **`avatar`** is present (including `{}`), nested values take precedence; legacy keys are not merged into an empty nested object.

---

## Avatar active (grace-mar `bot/avatar_controller.py`)

The avatar layer is **active** only when:

1. **`voice_avatar.enabled`** is `true`, **and**
2. **`avatar.enabled`** is `true` (after parsing; legacy configs infer enabled from `avatar_type != "none"`), **and**
3. **`avatar.type`** is not **`none`**.

---

## Emotion from critique score

**Precedence:**

1. **`avatar.emotion_mapping`** in runtime config → base label via `emotion_from_score()` in **`scripts/voice_runtime_config.py`**.
2. Else built-in defaults (same thresholds: 0.75 / 0.90, labels thoughtful / neutral / happy).
3. Then **`expression_scaffold.avatar_mapping.emotion_map`**: maps that base label to the renderer’s label.

**`emotion_mapping` shapes:**

- **Band-style:** `low_max_score`, `high_min_score`, `low_emotion`, `medium_emotion`, `high_emotion` (see example JSON).
- **Named confidence keys:** `low_confidence`, `medium_confidence`, `high_confidence` with optional `low_max_score` / `high_min_score`.

---

## `latency_mode` and constitutional critique

Call **`merge_critique_for_latency_mode(constitutional_critique, latency_mode)`** before applying critique in a voice path. It returns a **shallow copy** of the critique dict with adjusted fields:

| Mode | Effect (typical) |
|------|-------------------|
| **`balanced`** | Unchanged. |
| **`governed`** | Stricter: higher `trigger_threshold`, lower `long_response_chars`. |
| **`ultra_low`** | Relaxed: lower `trigger_threshold`, higher `long_response_chars`. |

Root **`monitoring`** is unchanged by this helper.

---

## Parser

**`scripts/voice_runtime_config.py`** is shared between **companion-self** and **grace-mar** (same file). **`parse_voice_avatar_block()`** returns structured defaults; **`merge_critique_for_latency_mode()`** implements the latency table above.
