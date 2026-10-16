---
review_id: "2026-10-16-003"
created_at: "2026-10-16T20:00:13+02:00"
reviewer: Codex
subject: "Optimate våg 3h — granskning av tre interna legacyprodukter"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Granskning av Optimate våg 3h, signal 002

Beräkningarna för Gotland taxa 21, Mölndal och Norrenergi är riktiga mot
handoffens oberoende facit. Den interna piloten innehåller exakt de tre nya
produkterna med `legacy_arskostnad`, den publika listan är fortsatt exakt 57
och inga tariffdata, prisformler eller kundvyer har ändrats. Codex omkörde
**232/232** riktade Neptune-prov, ren TypeScript-kontroll, grönt
produktionsbygge, **155/155** skills-prov plus fyra subtest,
matrisgeneratorns `--check` och rena diffkontroller. Dispositionen är rätt:
**57 publika / 3 interna / 1 prototyp / 16 ogranskade = 77**.

Leveransen kan ändå inte godkännas för aktivering ännu. Två uttryckliga
fail-closed-krav i handoffen är inte mekaniskt bundna på Neptune-sidan.

## P1 — legacy-backendens allowlist är inte bunden som en exakt mängd

`besparingsvarde.ts:1052–1059` har en privat `ReadonlySet` med sex ID:n.
Proven visar att de tre Wave-3h-ID:na och de tre äldre legacyprodukterna
räknar samt att tre valda kontroll-ID:n avvisas. De bevisar däremot inte att
allowlisten innehåller **endast** dessa sex. Ett sjunde, annat katalog-ID kan
läggas till utan att den fulla snapshotsviten faller, så de två separata
grindarna kan glida isär trots handoffens krav på en exakt, fail-closed
bindning.

Rätta detta utan att bredda produktionsscopet:

1. Gör legacy-ID-mängden maskinläsbar och oföränderlig, lämpligen som en
   exporterad fryst tuple med exakt Gotland taxa 17, Halmstad, Göteborg och
   de tre `WAVE_3H_PRODUCT_IDS`; härled backendens privata `Set` från denna.
2. Lägg ett prov som jämför hela tuplemängden mot exakt de sex tillåtna
   ID:na, kontrollerar unikhet/oföränderlighet och jämför den med exakt den
   delmängd av `SCENARIO_PILOT_TARIFFER_SNAPSHOT` vars backend är
   `legacy_arskostnad`. Ingen punktvis negativ sentinel får vara enda beviset
   för frånvaro av extra ID:n.
3. Behåll direkta negativa backendprov för okänt, kontraktsgatat och genuint
   ogranskat katalog-ID.

## P1 — råa tariffkontraktet är bara delvis bundet i Neptune

`optimateScenarioVag3h.test.ts:154–207` kontrollerar bara valda delar av de
tre katalogposterna. Exempelvis kontrolleras inte hela Mölndals eller
Norrenergis bandtabell, Gotlands justeringsenhet/mätgrund/formel,
justeringarnas exakta nyckelmängder, de fulla indatafältskontrakten eller de
exakta månadsprislistorna som råa katalogvärden. Facitproven verifierar
beräkningsresultatet, men kan inte ersätta handoffens separata krav att hela
råkontraktet binds i **både Neptune och skills**; kompenserande
katalogändringar eller extra nycklar kan annars passera Neptunes test.

Utöka Neptune-provet med oberoende literals och exakt djupjämförelse för
varje produkts beräkningsrelevanta råkontrakt:

- moms och exakt månadsprislista;
- hela kapacitetsobjektet inklusive typ, enhet, faktor, ordnad bandtabell
  och debiteringsgolv;
- fast avgift och månadsperiodisering;
- hela, ordnade justeringsobjekt med exakt nyckelmängd;
- exakt mängd indatafält samt nyckel, enhet, default, min/max,
  gissningsmarkör och heltalskrav;
- fortsatt avsaknad av kontraktspolicy och eligibility.

Skills-grinden och dess mutationsprov är i övrigt godtagbara och ska inte
skrivas om annat än om ett nytt prov visar en konkret lucka.

## P2 — stale och motsägande testtext

`besparingsvardeLegacyKostnadsledGate.test.ts:41` säger fortfarande att
backendens exakta mängd bara är Gotland taxa 17 och Halmstad trots att den
nu är sex produkter. Kommentaren vid Habo kallar dessutom samma objekt både
"legacy-eligible" och kontraktsgatat. Rätta rubrik och kommentarer så att de
beskriver den nya exakta sexmängden och kontrollobjektens verkliga roll.

## Rättningsscope

1. Ändra endast legacy-allowlistens representation/export, Neptune-prov och
   append-only bokföring. Tariffdata, formler och scenarioberäkning ska vara
   oförändrade.
2. Dispositionen ska förbli **57/3/1/16=77** och den publika listan exakt 57.
3. Kör riktade Wave-3h-/legacy-/snapshotprov, hela Vitest, ren
   TypeScript-kontroll, bygge med återställd `dist/`, skills pytest,
   generatorns `--check` och `git diff --check` i båda reporna.
4. Committera lokalt och lämna en ny unik `REVIEW_READY: Codex` med fulla
   hashar, ancestry och testutfall.

Ingen publik aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
