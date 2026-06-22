# Progression, Economy & Retention

For profitable 2D mobile games (casual / hypercasual / hybrid-casual / idle). For loop definitions → `01-design-foundations.md`. The monetization/ASO business side lives in the game-greenlight skill.

---

## 1. Loops and genre templates

- **Core loop** holds for 5 minutes, **meta loop** holds for 5 months (see 01).
- **Session loop:** the shape of a single session; end it in a way that **leaves the player wanting more**.

**Genre templates:**
- **Hypercasual:** Core = single tap/swipe → score. Meta is minimal (theme unlock, high score). (Stack: play → diamond → unlock theme.)
- **Puzzle/match:** Core = match → resource. Meta = spend → refresh/build + narrative (Homescapes).
- **Idle/incremental:** Core = tap/wait → earn → upgrade → earn faster. Meta = **prestige** resets give an earnings multiplier.
- **Merge:** Core = merge two low-tier items → higher tier → new chain. Meta = board expansion, orders, collection.
- **Builder/strategy:** Core = gather → build → fight → gather more. Meta = base progression, guild.

---

## 2. Progression systems

The "tour guide" that gates content and gives a continuous sense of advancement; it creates a sunk-cost investment.

**Types (mix several):** linear/vertical (power) · branching (skill tree, agency) · horizontal (variety without raising power: cosmetics, new mechanic) · collection/achievement/leaderboard/guild/narrative/building/time-gated.

**Rules:**
- **Align progression with the core mechanic** — it should extend it, not compete with it.
- **Unlock cadence = anticipation.** Keep exciting content "right around the corner"; there should always be a near-term goal.
- **Manage the mastery arc:** pre-mastery (frustration) → mastery (peak fun) → burnout (boredom). Introduce a new skill atom **before** the current skill becomes trivial; don't hide the fun behind grind that outlasts patience.
- **Visible milestones:** progress bar, level number, achievement list.
- **Skill vs grind balance:** progression shouldn't make skill irrelevant (the Fortnite Battle Pass keeps it cosmetic).
- **Prestige loops** for longevity (the D30 depth of idle): reset progress for a permanent multiplier.

---

## 3. Reward schedules (habit psychology)

| Schedule | Trigger | Effect | Example |
|---|---|---|---|
| **Fixed ratio** | After N actions | Predictable | Tetris points per line |
| **Variable ratio** | After a random number of actions | **Strongest habit; most resistant to quitting** | Loot/drop, crit, gacha, merge surprise |
| **Fixed interval** | Once per fixed duration | Predictable, session pacing | Daily login, +24h bonus |
| **Variable interval** | At random times | Rare on its own | Surprise bonus |

**Rules:** use **variable-ratio** for core excitement (loot, crit, merge surprise); use **fixed-interval** for habit/appointment (daily reward, energy). Layer them (daily login = fixed-interval, with random loot inside = variable-ratio) but test it. Match the reward type to the need (soft = progress, hard = premium/speed, cosmetic = expression, power = vertical, narrative = emotion). **Make the reward moment juicy** (sound/particles/animation). Daily reward + streak leverage loss-aversion — on the ethical edge (see §6).

---

## 4. Economy design

**"Inflation is the economy designer's enemy."** The job is to keep currencies **continually desirable**.

- **Soft currency:** earned through play (coins); sources: login, objectives, performance, idle. Broad spending: upgrades, items.
- **Hard/premium currency:** bought with money (gems); speed/exclusive/timer-skip.
- **Dual-currency:** non-payers progress with patience, payers with speed; both reach the same content.

**Sources (faucet):** login, level/objective, **idle/offline earnings**, ad reward, event.
**Sinks (drain):** power items, cosmetics, exclusives, timer skip, retry/continue.

**Rules:** balance faucet↔sink — enough should accumulate that it can be spent meaningfully, but not so much that purchasing becomes pointless. **Model the economy in a spreadsheet before shipping it** (play time required per level-up, earn/spend per session; simulate days/weeks). Add **deliberate sinks** against inflation (long upgrade ladders, cosmetics, prestige). **Idle/offline earnings = comeback hook** (usually capped at a few hours; the cap itself is a return-frequency lever).

---

## 5. Retention metrics & drivers

**Benchmarks (rising with UA costs):** classic D1 40% / D7 20% / D30 10%; D1 50%+ is now the bar. By genre: hypercasual ~D1 38–40%, D30 ~0; hybrid-casual ~D1 35–45% / D7 ~20% / D30 ~10%. **D1 mathematically caps D7/D30; D30 is the main indicator of long-term health.**

- **D1 (first impression):** onboarding quality, fast time-to-fun, clear guidance, low friction, the right audience (UA targeting). The 4 roots of bad D1: fun not found · player not guided to the fun · too many obstacles · wrong audience.
- **D7 (mid-game):** rewarding progression/meta (events, PvP, seasons), good content pacing (neither exhausted nor grind), social.
- **D30 (lifestyle integration):** meta depth (economy, social, complex systems), content variety + limited-time events, social pressure, accumulated investment (sunk cost).

**Session & comeback:** an energy/timer system paces the session (~5–20 min, every 4–8 hours; fits the lunch/evening rhythm). Comeback hooks: offline/idle earnings, daily reward, streak, energy refill, limited-time event. **Reward the return rather than punishing absence** (a healthier pull).

---

## 6. Ethics (and the 2025+ regulatory pressure)

- **Avoid dark patterns:** pay-to-skip the core challenge, forced grind, "play-by-appointment" (punishing absence), opaque currencies, gambling-like loot boxes, social coercion.
- In 2025 the UK/EU began scrutinizing these under consumer protection (especially loot boxes and obscured currency conversion, young audiences).
- **Healthy alternative:** reward presence instead of punishing absence; transparent currency/odds; generous offline earnings; optional (not mandatory) energy; progression that respects the player's time. Ethical retention + profitability are not in conflict (it lowers resentment-churn and regulatory risk).

---

## Sources

- Reward Schedules and When to Use Them — Game Developer: https://www.gamedeveloper.com/business/reward-schedules-and-when-to-use-them
- Power Progression in Games — Game Developer: https://www.gamedeveloper.com/design/power-progression-in-games-crafting-rewarding-player-experiences
- Progression Systems in Mobile Games — Udonis: https://www.blog.udonis.co/mobile-marketing/mobile-games/progression-systems
- The True Drivers of D1, D7, D30 Retention — Solsten: https://solsten.io/blog/d1-d7-d30-retention-in-gaming
- Building a Lasting Free-to-Play Economy — Mobile Free To Play: https://mobilefreetoplay.com/bible/building-lasting-free-play-economy/
- Game Economy Design in F2P — Machinations: https://machinations.io/articles/game-economy-design-free-to-play-games
- A Game of Dark Patterns — ACM: https://dl.acm.org/doi/fullHtml/10.1145/3491101.3519837
