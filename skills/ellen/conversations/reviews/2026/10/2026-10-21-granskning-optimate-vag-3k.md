# Optimate våg 3k — granskning av signal 2026-10-19-004

Status: `CHANGES_REQUIRED: Claude`. Granskare: Codex. Ingen aktivering eller push.

Granskat Neptune `3c3afa47afbdd45e0765d5a174014408aa124a91` (förälder `db218c0b4d8247a5577e4b6bc3cf980658dbf7a9`) och skills implementation `23d99b8fc38226388dbcb2520186518c2dee7daf`, logg-HEAD `ea9c63e`.

Den tidigare temporära Neptune-worktreen saknades. Granskningen utfördes på samma commit i en ny isolerad, detached worktree: `/Users/robertrennel/Code/neptune-review-vag-3k`. Ordinarie checkout och grenen har inte flyttats.

## Fynd

1. **P2 — Python-kontraktskontrollen är inte exakt.** I `generera_besparingspotential_tackningsmatris.py:2634` jämförs bara månadsvärdena inuti energiobjektet och i rad 2641 bara utvalda kapacitetsnycklar. Policykontrollen binder bara vissa av bindningarna. Oberoende mutationer av parsad, verklig snapshot accepterades av `build_matrix`: `kapacitet.unexpected=1`, `energi.unexpected=1` och `policy.kallenergi_bindning='flode_m3'`. Alla gav fortsatt 77 produkter. Uppdraget kräver hela råkontraktet utan extra egenskaper. Bind de fullständiga relevanta objekten och policybindningarna med strikt jämförelse och lägg negativa regressionsprov för varje kontraktsdel enligt handoffen.

2. **P2 — den globala accessfamiljen binds inte i Python.** Att lägga en kopia av Jönköpings `metered_access_fee` på `riksgenomsnitt` accepterades av `build_matrix`, fortfarande med 77 produkter. Neptune har ett globalt katalogprov, men Python itererar bara de förvalda Wave-3k-parametrarna. Härled hela mängden produkter med denna justering och kräv exakt `WAVE_3K_PRODUCT_IDS`; testa extra och saknad familjemedlem. Befintliga Pythonändringar lägger bara till medlemskaps-/statuskontroll, inte de beställda Wave-3k-mutationsproven.

3. **P2 — bandgränsprovet testar inte produktionsvägen.** `optimateScenarioVag3k.test.ts:508` anropar endast testfilens egen `kapacitetsled`. Kör de fyra literalgränserna genom den riktiga scenariovägen och kontrollera referens samt alla tre efter-scenarier. Lägg också det beställda negativa fallet med ett existerande men felaktigt band för angiven effekt, och icke-numerisk kapacitet. Pinna `kostnadsskillnadKr` direkt mot 6 033,20 / 9 049,80 / 12 066,40; nu kontrolleras bara positivitet och monotonicitet för det exponerade besparingsfältet. Bevisa att input och dess låsta kontraktsfält/proveniens förblir oförändrade, inte bara att summerade prisled sammanfaller.

## Verifierat

- Full Vitest: 3 787/3 787, 108 filer.
- `tsc --noEmit`: grön.
- `npm run build`: grön; byggändringar i spårad `dist` återställda i den isolerade worktreen.
- Python: 238/238 och 8 subtest via befintlig enkey-agents-venv (system-Python saknar pytest).
- Matrisgeneratorns `--check` mot granskad Neptune-snapshot: grön, 77 produkter och korrekt källhash.
- Commitdiffarnas whitespacekontroller: gröna.
- Intern pilot för Jönköping, oförändrad publik lista: 62 publika / 1 intern / 1 prototyp / 13 ogranskade.
- Handräknat bas-/scenariofacit verifieras av den befintliga sviten. Inget fel i nuvarande normalfallsbelopp påvisat.

## Avgränsad rättning

Claude rättar endast dessa verifierings-/matrisgrindar enligt handoff 2026-10-18-009. Ingen ändring av tariffdata, kostnadsmotor, kund-UI, publik aktivering, mainflytt eller push. Använd en separat implementation-worktree på Wave-3k-grenen; granskarens detached worktree ska hållas separat. Kör relevanta prov och full grind, skriv sedan en ny unik `REVIEW_READY: Codex` med fulla hashar och disposition.

## Återupptagande och anslutning

Robert: ”Gör det men kolla först att du kan nå claude, eller skall jag öppna cladue i ett nytt fönster?”

Claude Code 2.1.304 svarade `CLAUDE_OK` på ett verktygslöst anslutningstest. Inloggningen fungerar utanför sandboxen; sandboxens `auth status` gav felaktigt intryck av utloggning. Ingen ny interaktiv Claude-session behövs för CLI-kontakt. Bryggans status var `latest_id=2026-10-19-004`, `route=codex`, `claimed_id=2026-10-19-003`. Detta test startade inte någon bakgrundsbevakare eller implementation.
