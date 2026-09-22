---
session_id: "2026-09-22-005"
started_at: "2026-09-22T13:35:00+02:00"
last_updated: "2026-09-22T13:35:00+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: completed
topics:
  - Optimate
  - täckningsmatris
  - arkitekturgranskning
source: visible-conversation
transcript_fidelity: summarized
---

# Etapp 0: bevara Stockholmsprototypen och inventera portföljen

Robert: ”OK låter bra, kör!” — klartecken att utföra den föreslagna
inledande etappen för besparingspotential i alla godkända tariffer.

Codex har slutgranskat och lokalt committat exakt åtta sedan tidigare
opublicerade Neptune-filer för Stockholms rumsvärmeprofil och
Optimate-prototyp: `86be35ae4c5e3f021c97c40d0473ab3d3427b127`,
förälder `a4eb519e06bed0eaaa62719b87ee9e330b071529`. Rättningen
förtydligar att schablonens tappvarmvattenbaslast i totalvärmeläget
begränsas av respektive månads faktiska värmeköp; test med noll
sommarmånader ingår. Verifierat: 2 271/2 271 TypeScript-test, ren
`tsc`, isolerat `dist-eval`-bygge och Chromium-E2E 1–29 gröna.
Neptunes arbetskopia var ren efter commit; spårad `dist/` orördes.

Codex har också skapat en [maskingenererad täckningsmatris](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.md)
med [JSON-data](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.json),
[generator](../../../../Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py)
och sex godkända tester. Den binder den genererade 2026-snapshotens
SHA-256 och katalogproveniens och räknar 75 produktval: 74 verkliga,
ett syntetiskt; åtta med befintlig besparingsväg och 67 med enbart
kontraktsstyrd årskostnad. Alla nya scenariorader står kvar som
`not_reviewed`. `--check` bekräftar att Markdown och JSON matchar
snapshoten.

I [arkitekturgranskningen](../../../reviews/2026/09/2026-09-22-arkitekturgranskning-besparingspotential-etapp-0.md)
noteras att kostnadsprisled behöver exponeras från samma tariffmotor,
att effekt-/flödes-/retur- och historikantaganden inte får smyga in som
garanterad besparing, och att Vattenfalls profil-/behörighetsväg kräver
egen hantering. Rekommenderad nästa implementation är en typad gemensam
före/efter-motor bakom en separat scenarioförmåga, med Sundsvall
Indal/Liden/Lucksta som första enkel pilot och Stockholm som regression.

Ingen ny tariff eller scenarioförmåga har aktiverats. Ingen push har
gjorts. Inga orelaterade filer i den smutsiga skills-arbetskopian eller
andra repoändringar har tagits med. Den lokala förhandsvisningen på
`http://127.0.0.1:4174/kalkylator` var tillgänglig vid verifieringen.
