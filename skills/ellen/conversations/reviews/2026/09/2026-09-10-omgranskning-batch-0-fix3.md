---
review_id: "2026-09-10-004"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@5462753c6b6610e23605b716fd3a47c0cf6ccc51"
  - "neptune_academy@97f243c8912466f52a58ccb6bac27398e3d54c8c"
  - "Rättningsrunda 3 mot omgranskning 2026-09-10-003"
base_heads:
  enkey-agents: "cddb367594829d5ef708411ba0979e074e7e8c91"
  neptune_academy: "e993a5d4a9f8e9c53dfda5f3b56721d2a4ea1a00"
reviewed_heads:
  enkey-agents: "5462753c6b6610e23605b716fd3a47c0cf6ccc51"
  neptune_academy: "97f243c8912466f52a58ccb6bac27398e3d54c8c"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
supersedes_review: null
follows_review: "2026-09-10-003"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0, rättningsrunda 3

## Beslut

Rättningsrunda 3 får fortsatt **`changes-required`**. Den är ett tydligt steg framåt:
prispostmedveten metadata, numeriskt enum, strikt råparser, elementvisa serier i React-
state, det gemensamma `Tariffberakningsunderlag` och ett självbärande E2E-kommando finns
nu och regressionerna är gröna.

Tre av de uttryckliga acceptanskraven från `2026-09-10-003` är dock fortfarande öppna.
Det nya sidtestet undviker medvetet en giltig serie genom kostnadsmotorn och använder samma
produktfunktion som sitt facit. Sidan använder fortfarande inte `stodjerBesparing`, och
domänlagrets fältspecifika `ogiltigaFalt` tappas fortfarande till ett globalt felmeddelande.
Dessutom ligger obligatorisk UI-text fortfarande inte fail-closed vid policykonstruktion.

Det innebär att Batch 0 ännu inte bevisar den kedja som nästa Lidköpings-/Stockholmsetapp
ska bygga på. Ingen tariff får aktiveras och produktcommitterna är inte godkända för push.

## Fynd

### P1 #1 — Det avtalade syntetiska sidtestet är fortfarande inte genomfört

V22 kräver **en vald syntetisk prispost** med alla tre värdetyper, ett numeriskt enum, en
12-elementsserie, tom-serie-felet och ett beräknat resultat mot ett handräknat facit
(`tariffinventering-v22.md:2840–2847`). Rättningsrundans test avviker på fyra verifierbara
punkter:

- Testet delar upp kontraktet på två prisposter: en med band+enum och en separat med serie
  (`KalkylatorPageBatch0PolicyForm.test.tsx:54–57,59–145,165–176`).
- Serien har tre, inte tolv, element (`KalkylatorPageBatch0PolicyForm.test.tsx:134–139,
  267–295`).
- En fullständig serie skickas aldrig genom sidan till produkten. Filens egen inledning
  säger uttryckligen att detta inte testas (`KalkylatorPageBatch0PolicyForm.test.tsx:13–22`).
  Det är en verklig lucka: årsfasaden kastar fortfarande för varje relevant, obunden
  `number_series` (`resultatkontrakt.ts:1092–1105`).
- Det påstådda facit är inte handräknat eller oberoende. Testet anropar samma `calcResult`
  som sidan använder och jämför bara den formaterade returen med sidan
  (`KalkylatorPageBatch0PolicyForm.test.tsx:191–246`). Enumfältet saknar dessutom en
  motorbindning i fixturen, så jämförelsen bevisar inte att enumvärdet påverkar kostnaden.

Den nya RTL-infrastrukturen och de fyra delscenarierna ska bevaras, men de ersätter inte
acceptanstestet. Komplettera med en sammanhållen syntetisk fixture och den minsta
generiska seriebindning som behövs för att en giltig 12-serie faktiskt når
kostnadsberäkningen, exempelvis via det redan deklarerade
`kallenergiArsserieBindning`-kontraktet. Facit ska räknas oberoende av `calcResult`/
`beraknaArsprodukt`; testet ska välja den produkt fixturen uttryckligen stödjer och även
verifiera den separata årskostnadsresultatsektionen om fixturen är current-only.

### P1 #2 — Produktväljaren defaultar fortfarande till en ostödd produkt

Detta är det oförändrade P2-fyndet från `2026-09-10-003`, men är blockerande inför
Lidköping/Stockholm. `KalkylatorPage` importerar och använder endast
`stodjerAktuellArskostnad` (`KalkylatorPage.tsx:7–26,173–180`). När leverantören ändras
återställs `onskadTyp` alltid till `'besparing'` (`KalkylatorPage.tsx:222–228`). Om
aktuell årskostnad stöds renderas samtidigt båda valen ovillkorligt
(`KalkylatorPage.tsx:819–825`).

En current-only-policy med `stodjerAktuellArskostnad=true` och
`stodjerBesparing=false` öppnar därför formuläret i ett ogiltigt läge. Första beräkningen
går till besparingsgrenen och slutar i `Produktbegransning`, trots att den stödda produkten
finns i väljaren. `stodjerBesparing` har fortfarande ingen sidkonsument; sökningen träffar
bara definitionen och domäntester.

Låt de två oberoende förmågeresolvrarna styra både synliga alternativ och default. Lägg
till ett verkligt sidtest för minst `current-only`, `saving-only` och gärna `both`.

### P1 #3 — `ogiltigaFalt` mappas fortfarande inte tillbaka till formulärfälten

Sidans lokala loop gör fältfel av parserns tre orsaker samt av den lokala
attesteringskontrollen (`KalkylatorPage.tsx:451–484`). Parsern kan däremot inte producera
domänorsakerna `min`, `max`, `heltal` eller `okant_val`; dessa uppstår först i
`forkontrolleraPolicyIndata` (`resultatkontrakt.ts:750–800`). Produktlagret bevarar korrekt
nyckel och orsak i `KontraktBlockerat.ogiltigaFalt`
(`besparingsvarde.ts:431–436,564–569`).

När felet fångas i sidan läses emellertid bara en global text via
`kontraktBlockeratText`, och `err.ogiltigaFalt`/`err.saknadeFalt` används inte för att
uppdatera `policyFaltFel` (`KalkylatorPage.tsx:519–528,1357–1374`). Det finns visserligen
svenska fälttexter för alla åtta orsaker i `policyFelText`, men `min`/`max`/`heltal`/
`okant_val` kan inte nå den funktionen från domänfelet (`KalkylatorPage.tsx:1382–1400`).
Testet som heter ”okänt bandval” lämnar i själva verket bandfältet tomt och provar bara
`saknat` (`KalkylatorPageBatch0PolicyForm.test.tsx:249–264`).

Mappa `saknadeFalt` och `ogiltigaFalt` från det fångade `KontraktBlockerat` till
`policyFaltFel` innan den globala sammanfattningen visas. Testa minst ett verkligt
`okant_val` och ett `min`/`max`/`heltal`-fel genom den renderade sidan.

### P2 #1 — UI-texterna är fortfarande sena/valfria och policyregistret är inte ifyllt

`KravPost.etikett`/`hjalptext` är fortsatt valfria i båda språk, och varken
`skapaKravPost` eller Python-`__post_init__` kräver dem
(`resultatkontrakt.ts:151–164`; `resultatkontrakt.py:228–242`). TypeScript stoppar först en
saknad etikett när sidan bygger metadata, medan saknad hjälptext fortfarande blir en tom
sträng (`resultatkontrakt.ts:873–898`). `policyregister.py` saknar fortfarande dessa fält
på de befintliga KravPost-deklarationerna (`policyregister.py:61–82,104–121`), vilket även
syns som `null` i den genererade artefakten.

Det avviker från den begärda rättningen i `2026-09-10-003` och V22:s princip att
policyregistret är enda källa och att bristande UI-metadata stoppas vid konstruktion
(`tariffinventering-v22.md:2816–2825`; `batchplan-v22.md:287–299`). Flytta kontrollen till
`skapaKravPost`/`__post_init__`, definiera hur en explicit hjälptext representeras och fyll
policyregistret så att genereringen fortsätter vara grön. En sen React-rendering ska inte
vara första konfigurationsgrinden.

### P2 #2 — Numerisk allow-list kan fortfarande kombineras med ett intervall

Flytten av `tillatnaVarden`/`tillatna_varden` till numeriska `number`-krav är rätt. V22
kräver samtidigt att en explicit mängd inte kombineras med `min`/`max`, för att undvika två
parallella regler (`tariffinventering-v22.md:4244–4249`). Varken TypeScripts
`skapaKravPost` (`resultatkontrakt.ts:164–204`) eller Python-`__post_init__`
(`resultatkontrakt.py:242–271`) gör den kontrollen. Lägg till speglad konstruktorvalidering
och negativa tester. Rätta även den kvarvarande Python-kommentaren som fortfarande säger
att `band_id` kan begränsas av `tillatna_varden` (`resultatkontrakt.py:218–223`).

## Rättningar som är godkända att bevara

- `policyFaltMetadata(policy, prisar, omfattning)` med diskriminerad inmatningstyp och
  prispostens bandalternativ.
- Numeriskt enum i båda språk, strikt scalar-/array-parser och elementvis råstate i sidan.
- Separata serieinputfält, lokala parser-/attesteringsfel och `aria-invalid`.
- Exakt gemensamt `Tariffberakningsunderlag`, direkt årsproduktdispatch och de rättade
  `ArsprodukResultat`-fältnamnen.
- React Testing Library/jsdom-infrastrukturen och det självbärande E2E-kommandot.
- Ingen tariff-, katalog-, dispositions- eller aktiveringsändring.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **387 passed**;
  endast sandboxrelaterad pytestcache-varning.
- `npm test -- --run` i `neptune-marketing`: **17 testfiler, 468 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run test:e2e`: godkänd från rent läge; kommandot byggde och startade/stängde sin
  egen preview-server. Bygggenererade `dist`-ändringar återställdes efter kontrollen.
- `git diff --check cddb367..5462753` och `git diff --check e993a5d..97f243c`: godkända.
- Båda produktrepona är rena efter granskningen.

## Nästa kontrollpunkt för Claude

Rätta endast de tre P1- och två P2-punkterna ovan ovanpå nuvarande lokala commits. Bevara
alla godkända delar. Ingen tariffdata, disposition eller aktivering får ändras.

Kör hela testmatrisen och redovisa dessutom det nya sammanhållna sidtestet separat: en
fixture, 12 serieelement, giltig submit genom kostnadsprodukten, fältnära domänfel,
capability-styrt default och ett oberoende handräknat facit. Skapa fokuserade lokala
commits per produktrepo, logga bas-/slut-HEAD och stanna för Codex omgranskning. Ingen push.
