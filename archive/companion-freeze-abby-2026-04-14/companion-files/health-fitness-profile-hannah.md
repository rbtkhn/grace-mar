# Health-Fitness Profile — Hannah

**work-health-fitness user.** Companion-led. Phase 0 (Record-only). See [work-health-fitness](../../docs/skill-work/work-health-fitness/README.md).

**Data sources:** RENPHO body fat scale; Apple Watch / Apple Health (workouts, heart rate, HRV, sleep). All data for reference only; not for medical or health decisions.

---

## 1. Identity Linkage

```yaml
record_id: grace-mar
client_name: "Hannah"
birthdate: null   # add when documented
age_years: null   # add when documented; body age from scale: 34 (metric only)
reference_chart: null
```

---

## 2. Body Composition (RENPHO scale)

**Measurement:** Mar 4, 2026, 9:39 AM.

| Metric | Value | Assessment |
|--------|--------|------------|
| Weight | 114.4 lb | Standard |
| BMI | 18.6 | Standard |
| Body fat | 21.2 lb, 18.5% | Robust/Strong |
| Subcutaneous fat | 17.7% | Low (1 item not up to standard) |
| Skeletal muscle rate | 54.2 lb, 47.5% | Standard |
| Fat-free mass | 93.2 lb | — |
| Visceral fat | 2 | Excellent |
| Body water | 63.8 lb, 55.9% | Standard |
| Muscle mass | 87.6 lb, 76.6% | Standard |
| Bone mass | 5.6 lb, 4.9% | High |
| Protein | 22.6 lb, 19.7% | High |
| Basal metabolic rate | 1284 kcal | Standard |
| Body age | 34 | Excellent |

*RENPHO data for reference only; not for medical or health decisions.*

---

## 3. Movement & Workouts (Apple Watch / Health)

### Sample workouts (logged)

| Date | Activity | Duration | Distance | Calories (active) | Avg HR | Notes |
|------|----------|----------|----------|-------------------|--------|-------|
| Mar 6, 2026 | Outdoor Cycle | 22 min | 4.80 mi | 156 | 158 BPM | 9:00–9:22 AM; speed 13.0 MPH; HR range 107–171 |
| Mar 6, 2026 | Yoga | 26 min 27 sec | — | 85 | 113 BPM | Highlands Ranch; 9:45–10:11 AM; HR ~94–133 |

### Documented activities

- Outdoor cycling
- Yoga

```yaml
movement:
  documented_activities: [Outdoor Cycle, Yoga]
  goals: []  # companion adds
```

---

## 4. Heart Rate (Apple Health, Apr 2025 – Apr 2026)

| Context | Range |
|---------|--------|
| Overall (yearly) | 39–181 BPM |
| Resting | 58–67 BPM |
| Walking average | 80–96 BPM |
| Workout | 63–181 BPM |

*Latest recorded (from screenshot): 62 BPM at 1:44 PM.*

---

## 5. Cardio Fitness (Apple Health, Mar 2025 – Mar 2026)

- **Average level:** Above Average (7 months in period).
- **Trend:** Cardio fitness index ~33 (Mar 2025) to ~38–39 (Feb 2026); sustained in or above “Above Average” range.

---

## 6. Heart Rate Variability (HRV, Apple Watch)

- **Average HRV:** 37 ms (Apr 2025 – Apr 2026).
- **Monthly trend (approx.):** 35–48 ms; higher in late 2025 (Sep–Oct ~45 ms), lower in Jan–Feb (~33–35 ms), rebound Mar ~48 ms.

*HRV from Apple Watch; validated for users 18+.*

---

## 7. Sleep (Apple Health, 6 months: Sep 7, 2025 – Mar 7, 2026)

| Metric | Value |
|--------|--------|
| **Average time asleep** | 7 h 54 min |
| Average awake | 29 min |
| Average REM | 1 h 50 min |
| Average core | 5 h 14 min |
| Average deep | 46 min |

```yaml
sleep:
  documented: true
  avg_asleep: "7h 54m"
  stages: { awake: "29m", rem: "1h 50m", core: "5h 14m", deep: "46m" }
```

---

## 8. Preferences & Goals (Companion-Led)

*From survey (Mar 2026).*

| Topic | Response |
|-------|----------|
| **Primary goal** | Feel stronger or more capable in daily life |
| **Movement frequency** | Most days (5–7 per week) |
| **Biggest barrier** | Motivation or energy |
| **Support style** | *(skipped)* |
| **Nutrition in profile** | Yes — include basics (goals, preferences) |
| **Sleep** | Mostly good — satisfied |
| **Rest days** | Plans them (e.g. same days) AND takes when tired/busy |
| **Best time to move** | Morning |

```yaml
sleep:
  documented: true
  satisfaction: "mostly good"
  goals: []

movement:
  documented_activities: [Outdoor Cycle, Yoga]
  target_frequency: "5-7 days/week"
  preferred_time: "morning"
  primary_goal: "feel stronger, more capable in daily life"
  biggest_barrier: "motivation or energy"
  rest_days: "planned AND when tired/busy"
  goals: []

nutrition:
  documented: true   # include basics, goals, preferences
  goals: []

recovery:
  documented: true   # rest-day approach above
  approach: "planned rest + responsive to fatigue"
```

---

## 9. Wisdom Questions (Optional)

Use when Hannah consents:

- How did you sleep last night?
- What movement felt good today?
- What did you eat that made you feel strong?
- Do you want a lighter or more active lesson today?

---

## 10. Integration Notes

| Flow | Use |
|------|-----|
| Lesson prompts | Use sleep/movement data for intensity (e.g. lighter after low sleep); respect preferences. |
| Wisdom questions | Ask when Hannah opts in. No prescription. |
| Checkpoint reflections | Invitational only (e.g. “How did rest and movement go this week?”). |

**Guardrails:** Meet where they are (AGENTS rule 7). Companion-led. No prescription. Any new health-derived content for SELF/EVIDENCE goes through RECURSION-GATE.

---

*Populated from RENPHO and Apple Health screenshots; preferences from survey (Mar 2026). Last updated: 2026-03-09.*
