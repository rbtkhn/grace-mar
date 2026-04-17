# Seed Survey — Capture Template

Use during Session 001 to log responses and know where each goes.

---

## Pre-Session Checklist

- [x] self.md identity fields filled (name, birthdate, languages, location)
- [x] Parent has read docs/parent-brief.md
- [x] Consent logged in session-log.md
- [x] Capture method ready: parent typing

---

## Question → Destination Map

| # | Question | self.md destination | Notes |
|---|----------|---------------------|-------|
| 1 | Favorite movies/shows? | `II.PREFERENCES.movies` | List as provided |
| 2 | Favorite books/stories? | `II.PREFERENCES.books` | List as provided |
| 3 | Favorite places? | `II.PREFERENCES.places` | List as provided |
| 4 | Favorite games? | `II.PREFERENCES.games` | List as provided |

---

## Capture (fill during session)

### Q1: Favorite movies or shows?
```
Frozen, Thomas the Train, Land Before Time, E.T., Moana, Mickey Mouse, Paw Patrol, Mulan
```

### Q2: Favorite books or stories?
```
Berenstain Bears, Madeline, Hans Christian Andersen Fairy Tales, Grimm Fairy Tales,
Clifford the Big Red Dog, The Very Hungry Caterpillar, Coat of Many Colors,
Hooper Humperdink
```

### Q3: Favorite places?
```
Elitch Gardens, The Broadmoor, Anyang China, Cancún Mexico, Los Cabos Mexico,
Paintbrush Park, San Diego
```

### Q4: Favorite play/activities? (substituted for "games")
```
Gymnastics, soccer, basketball, skateboard, swimming, climbing, trampoline,
legos, art, drawing
```

---

## Post-Session Updates

1. **self.md** — Paste responses into `II. PREFERENCES > Favorites` YAML:
   ```yaml
   movies: [list from Q1]
   books: [list from Q2]
   places: [list from Q3]
   games: [list from Q4]
   ```
2. **self.md** — Set `survey_completed: true` in XII. METADATA
3. **session-log.md** — Add SESSION 001 block with date, participants, responses, updates
4. **survey-capture.md** — Optional: keep for reference or delete after data migrated
