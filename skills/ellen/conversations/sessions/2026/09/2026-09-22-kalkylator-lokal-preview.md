---
session_id: "2026-09-22-001"
started_at: "2026-09-22T08:48:23+02:00"
last_updated: "2026-09-22T09:55:15+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: active
topics:
  - kalkylator
  - lokal förhandsvisning
source: visible-conversation
transcript_fidelity: summarized
---

# Kalkylatorn startad för fortsatt test

Robert bad att få kalkylatorn igång igen för mer testning. Den opublicerade
Stockholm Exergi-/Optimate-koden från 2026-09-21 finns kvar i Neptune på
`main@a4eb519` med samma åtta lokala käll-/testfiler. `npm run eval:build`
byggde den isolerade `dist-eval/` utan fel (inklusive ren `tsc`).
Förhandsvisningen startades på
`http://127.0.0.1:4174/kalkylator` och HTTP-kontrollen gav 200.

Detta återupptar endast lokal testning. Ingen källkod, tariffaktivering,
commit eller push ändrades. Git-listan i handoff
`2026-09-21-paus-stockholm-optimate.md` gäller fortfarande efter att
testningen är klar. Port 4174 hålls öppen tills vidare.

## Fråga om leverantörstäckning

Robert frågade om endast Stockholm Exergi kan visa besparingspotential.
Kodkontroll av den genererade 2026-tariffilen och produktförmågan visar att
den **nya separata Optimate-vyn med 15/20/25 procent och villkorad
effektkänslighet** i dag bara finns för Stockholm Exergi. Den äldre
före/efter-besparingsvägen finns för åtta leverantörsval: riksgenomsnittet,
Göteborg Energi, Gotlands Energi taxa 17 och taxa 21, Halmstads Energi och
Miljö, Mölndal Energi, Norrenergi samt Sandviken Energi Helleverans.
Övriga kontraktsstyrda 2026-tariffer är i dagsläget spärrade för
besparingsprodukten och erbjuder uppskattad aktuell årskostnad. Ingen
funktion eller tariff ändrades med anledning av denna kontroll.
