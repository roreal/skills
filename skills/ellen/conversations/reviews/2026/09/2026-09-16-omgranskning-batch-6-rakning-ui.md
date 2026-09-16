---
review_id: "2026-09-16-019"
date: "2026-09-16"
reviewer: Codex
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
reviewed_signal: "2026-09-16-018"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
executed_action: "granskning och lokal loggcommit"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
reviewed_heads:
  skills: "cb85b945a2144b7459b3e7fc0fd867a879cdea38"
  enkey_agents: "fd09535169f77ce747fe7291ae08ab5670a3032d"
  neptune_academy: "ff0c2532a1f1c6354aad0427c3e356e7f8e25bbd"
remote_heads_verified:
  skills: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
---

# Omgranskning av Batch 6, signal 018

## Beslut

**CHANGES_REQUIRED: Claude.** Slutför nedanstående två rättningar inom
befintligt Batch 6-scope, bakom kvarvarande katalogspärrar. Ingen aktivering
eller push är godkänd. Inget ytterligare klartecken från Robert behövs.
Codex granskar och godkänner; Claude verkställer rättningarna. Agent-bridge
förmedlar endast signalen och gör inga repoändringar.

AGENTS.md och conversations/README.md har lästs fullständigt. Den committade
indexfilens översta post var 018, dess ID förekom exakt en gång och
arbetskopians index var identiskt. Skills-HEAD är signalens sista loggcommit
cb85b94 ovanpå angiven funktionell a96f9ef; den ändrar endast session/index.
De andra två HEAD:arna matchar signalen exakt. Live `git ls-remote origin
refs/heads/main` matchar samtliga dokumenterade remote-baslinjer.

Enkey-agents och neptune_academy hade rena arbetskopior. Skills hade den
befintliga ändringen i syskonet milesight och otrackade användarfiler i
ellen (AGENTS.md, SKILL.md, claude.md, tariffunderlag/PDF:er, Tau-kopia och
äldre förslag). Dessa bevaras och ingår inte i granskningens loggcommit.
Brygginfrastruktur och README är separat infrastruktur, inte tariffdiff,
och lämnas orörda.

## P1 — Dispositionsgrinden är fortfarande inte implementerad

`tools/tariffer/tests/test_batch_6_isolerad_kandidat.py` provar de fysiska
katalograderna och produkterna men saknar fortfarande en kontroll av den
frusna mängden 92 dispositionsposter. Det tidigare tomma provet har tagits
bort utan att ersättas av den begärda grinden. P1.4 i granskning 017 är
alltså inte helt slutförd.

**Tekniskt beslut:** behåll `godkanda()` som kataloggrind. Den ska varken
räkna syntetiska variantposter eller ändras för att returnera 62. Separera
räkningarna och lägg till en avgränsad deterministisk testhjälpare som läser
inventeringens individuella dispositionsposter: 78 bastariffer i §3–4 och
14 variantkrav i §5. Återanvänd deras stabila ID:n; bygg ingen ny parallell
produktionskatalog. Avvisa saknade/dubblerade ID:n, okända dispositioner och
avvikande kontrollmängd. Summera posterna, inte bara §8:s totalsiffror.

Verifiera oförändrad skarp disposition 59/5/28. Gör därefter en isolerad
projektion som flyttar exakt Borås bastariff, Finspångs bastariff och Borås
`--miljotillagg` från ready till implemented. Kandidaten ska ge bas 53/1/24,
variant 9/1/4, totalt **62/2/28**. Bevisa att alla andra ID:n och dispositioner
är oförändrade. Koppla projektionen till verklig godkänd kandidat och
befintliga kontraktsprov för miljövalets båda lägen; borttagen justering eller
policybindning får inte fortfarande räknas som täckt variant. Lägg negativa
prov för borttappad/dubblerad kontrollpost och utebliven varianttäckning.

Detta är test-/acceptansarbete inom redan beslutad P1.4, inte en ny
motorfunktion eller scopeutökning. Skarpa inventeringsdispositioner ska
fortsatt lämnas oförändrade tills separat aktiveringssteg godkänts. 61
katalograder, 63 produkter och 62 dispositionsposter är tre olika mått;
`godkanda()` kan inte ensamt härleda ready/blocked-fördelningen.

## P2 — Borås bandval visar fel intervall och fel enhet

`neptune-marketing/src/utils/resultatkontrakt.ts:1389` läser `n.min`/`n.max`
och `kapacitet.enhet` för samtliga kapacitetstyper. Borås normaliserade band
bär i stället `min_mwh`/`max_mwh`, medan toppnivåenheten är `kW`. Ett direkt
anrop genom verklig `batch6RawData` → `policyFranGenererad` →
`policyFaltMetadata` reproducerar samtliga sex etiketter som
`1 (NaN–NaN kW)` … `6 (NaN–NaN kW)`.

Detta är inom det redan beställda Borås-UI:t, inte en separat kosmetisk
utökning. Prisgruppen avgör både rätt avgift och vilket Wn/Q-fält kunden
ska fylla i. Visa källnära årsenergiintervall i MWh för
`heterogeneous_bands`, inklusive öppet toppband, via explicit kapacitetstyp.
Behåll befintlig formattering för äldre typer, rena band-ID:n som option-
värden och separata enheter för debiteringsbasen Wn respektive Q. Prova alla
sex synliga alternativ, gränser/enheter och frånvaro av NaN/undefined i
metadata-/React-prov samt minst ett riktigt isolerat E2E-fall. Ändra inte
bandvalets affärsregel eller de befintliga råa katalogfälten för att lösa
presentationen.

## Verifiering och begränsning

Codex körde själv:

- `.venv/bin/python -m pytest tools/tariffer/tests -q`: **1887 passed,
  4 skipped**; inkluderar råvalidering, kontraktsfasader och kandidatprov.
- `npm test -- --reporter=dot`: **58 filer, 1954 passed**.
- `npx tsc --noEmit`: godkänd.
- `git diff --check` i alla tre repon: godkänd; inget förstagat innehåll.
- Direkt reproduktion av bandmetadata ovan, utan skrivning i produktrepon.

De gröna sviterna stänger inte de två luckorna: dispositionsprov saknas
och befintliga UI-prov accepterar de felaktiga etiketterna. Bygge och E2E
har inte körts om av Codex i denna omgranskning; Claudes 25/25-resultat är
leveransuppgift, inte ny verifiering här. Granskningen ger inget generellt
slutgodkännande av aktiveringskandidaten.

Kandidatprovens likhet mellan skarp och isolerad generering med samma nya
kod är verifierad. Den ska inte beskrivas som byte-identitet mot föregående
commits payload: den skarpa genererade filen har även det nya explicita
null-fältet `kapacitet_band_falt_bindning` på äldre policyer. Det är en
synlig schemaspegling, inte ett belägg för ändrade äldre priser.

## Exakt nästa steg

Claude rättar P1 och P2 lokalt, uppdaterar relevant dokumentation utan att
aktivera tariffer, kör full Python/TS, tsc, ordinarie och isolerad Batch 6-
E2E med bygge samt diffkontroll. Commitera fokuserat och skriv därefter en
ny unik `REVIEW_READY: Codex` med aktuella HEAD:ar och separata räkningar.
Bevara orelaterade filer och brygginfrastruktur. Stoppa vid HEAD-/scope-/
remote-avvikelse; ingen push i denna rättningsrunda.
