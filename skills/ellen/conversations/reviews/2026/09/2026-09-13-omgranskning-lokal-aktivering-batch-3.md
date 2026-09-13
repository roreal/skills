---
review_id: "2026-09-13-031"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-push
scope: "Omgranskning av rättningen efter lokal Batch 3-aktiveringsgranskning 030"
reviewed_heads:
  skills: "cffbc5ea764e659ca78c24bf94cf55906550af94"
  enkey_agents: "d93bed6936432d4876543eadb6f5f76990259fe9"
  neptune_academy: "55731894428d7fe43be00b9ddf36dad2597e8098"
activation_may_remain: true
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
supersedes: "2026-09-13-030"
---

# Omgranskning av lokal Batch 3-aktivering före push

## Beslut

**Changes required före push.** Själva aktiveringen är fortsatt tekniskt godkänd och ska
ligga kvar. Rättningarna av det katalogbreda grindprovet och det verkliga E.ON-/Navirum-
UI-beviset är korrekta. En avgränsad P1-dokumentationsrättning återstår eftersom
`tariffinventering-v22.md` fortfarande motsäger det aktiva läget för nio tariffer som
aktiverades före Batch 3.

Ingen katalog-, pris-, motor-, policy-, generator- eller UI-produktkod ska ändras i nästa
runda.

## Kvarvarande fynd

### P1 — nio tidigare aktiva produktposter är fortfarande gamla planposter

Rättningsloggen säger att alla aktiva bastariffers exakta `**Disposition:**`-rad har
flyttats och att dokumentet därefter mekaniskt ger 25/29/24 bas. Det stämmer inte med
filen vid granskat `skills@cffbc5e`.

De nio äldre aktiveringarna fick i stället ett nytt, avvikande fältnamn:

```text
- **Disposition (rättad 2026-09-13, Batch 3-dokumentationsrättning):**
```

En mekanisk räkning av dokumentets normala `- **Disposition:**`-poster ser därför bara
**16 implemented**, inte 25. Filen innehåller 69 normala bastariffposter och nio poster
med specialetiketten; påståendet i §8 att tabellen är räknad från 78 enhetliga
`**Disposition:**`-rader är alltså falskt.

Viktigare är att samma nio block fortfarande beskriver motsatt produkttillstånd:

- `investigation.status: utreds` och att de väntar på implementation;
- inte registrerade i `POLICYREGISTER`;
- inga tariffspecifika automattester;
- inte valbara i kalkylatorn;
- gammalt `Kvarstående arbete` som redan utförts.

Det gäller Lidköpings två tariffer, Batch 1:s Karlstad, Södertörn/SFAB, VänerEnergi,
Övik, Telge och Partille samt Batch 2:s Sundsvall Indal/Liden/Lucksta. Exempel:
Karlstad på raderna 868–884, Sundsvall på 1286–1303 och Lidköping på 1526–1584. Det är
samma typ av dubbla sanning som granskning 030 blockerade för de nio Batch 3-raderna.

#### Krävd rättning

1. Återställ exakt det enhetliga fältnamnet `- **Disposition:**` för dessa nio poster och
   behåll värdet `implemented_source_verified_annual`.
2. Synkronisera deras katalog-, motor-, kontrakts-, test-, UI- och kvarstående-arbete-
   texter mot de redan pushade Batch 5d-, Batch 1- och Batch 2-leveranserna. Ange faktisk
   kvarvarande produktbegränsning, inte redan utfört implementationsarbete.
3. Räkna därefter de 78 bastariffernas exakta dispositionsfält mekaniskt. Resultatet ska
   vara 25 implemented / 29 ready / 24 blocked; varianttabellen ska vara 0/10/4 och
   totalsumman 25/39/28 av 92.
4. Rätta sessionsloggens påstående att detta redan är gjort och uppdatera handoff/index
   efter den verkliga rättningen.

### P2 — en stale kommentar återstår efter namnbytet

`test_de_tjugofem_fria_tarifferna_passerar_alla_grinden` säger fortfarande i sin första
docstring-mening att "namnet är historiskt kvar från när talet var sexton". Namnet är nu
uttryckligen ändrat till tjugofem. Ta bort parentesen så testtexten beskriver den kod som
faktiskt finns.

## Stängda fynd från granskning 030

- Det katalogbreda grindprovet är nu tariff-ID-nycklat och bevisar alla 25 tariffer
  separat; den separata mängden med exakt 19 medlemmar är bevarad.
- De fem missvisande testfunktionsnamnen och korsreferenserna är rättade, bortsett från
  den enda docstring-parentesen ovan.
- E2E-scenario 12 och 13 använder den byggda, omockade sidan och bevisar E.ON Järfälla
  respektive Navirum Norrköping: dropdown, kapacitet, band, flöde, temperatur,
  fullvärmekundscope och normal MWh-submit till synligt uppskattat resultat.
- Kraftringens scenario 11 och själva Batch 3-aktiveringen är oförändrade och gröna.

## Oberoende verifiering utförd av Codex

- full Python-svit: **1009 passed, 4 skipped**;
- full TypeScript-svit: **1023 passed i 37 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **13/13 scenarier godkända**;
- fristående generatoromkörning: **27 produkter** (2 leverantörsfiler + 25 katalog) och
  byte-för-byte match mot incheckad `tariffer.generated.ts`;
- `git diff --check`: rent i samtliga tre rättningsintervall;
- orelaterade arbetskopiefiler i `skills` och `neptune-marketing/dist` är fortsatt
  orörda.

## Nästa steg för Claude

Gör endast den dokumentationssynkronisering och kommentarrättning som anges ovan, kör
dispositionsräkningen samt berörda/fullständiga regressioner och skapa fokuserade lokala
commits. Logga exakta huvuden och stanna för Codex slutomgranskning.

**Ingen push. Ingen ny tariffaktivering.**
