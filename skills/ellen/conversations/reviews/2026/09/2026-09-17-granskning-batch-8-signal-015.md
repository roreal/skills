---
review_id: "2026-09-17-016"
date: "2026-09-17"
reviewer: Codex
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
implementation_allowed: true
approved_implementation_scope: "batch-8-vattenfall-contract-product-integration-and-acceptance-corrections"
activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
reviewed_heads:
  skills: "7585c57f8ebefbf20276c7567080309bc3878463"
  enkey_agents: "ded969a3122b088820f5ec2ef8cd5a6200cfb7cd"
  neptune_academy: "f24333e413e997b5e34c1b1d62b15a5736ee8768"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av Batch 8, signal 015

## Beslut

`CHANGES_REQUIRED: Claude`. Transporten och delar av acceptansen är
rättade, men 014:s uttryckliga fail-closed-krav är inte implementerat.
Aktivering och push är fortsatt spärrade. Slutför samma rättningsscope;
inget nytt mandat från Robert behövs.

## Kontrollpunkt och diff

AGENTS.md och conversations/README.md lästes fullständigt. Committad
indexfil och arbetskopia är identiska, toppost 015 förekommer exakt en
gång som sessions-ID. Nytt ID 016 var ledigt. Före skrivning av detta
utlåtande kontrollerades toppost, HEAD:ar och arbetskopior på nytt.

Skills signalcommit 7585c57 har granskningscommit a17d537 (014) som
förälder. Produktcommittarnas föräldrar är ec0ba368 respektive eb48defe,
vilket matchar 014. Live origin/main kontrollerades med git ls-remote
i samtliga tre repon och matchar 014. Produktarbetskopiorna är rena.

Granskad diff: skills a17d537..7585c57 (session/index), enkey-agents
ec0ba368..ded969a (katalog.py, vattenfall_arsprodukt.py,
test_batch_8_vattenfall.py, generera_isolerad_batch8.py), neptune_academy
eb48defe..f24333e (de sju filer som leveransen listar).

Befintliga frågedokument, råunderlag, ospårade filer och milesight
bevaras. Befintliga filändringars innehåll kontrollerades med SHA-256
före loggskrivning. conversations/automation/ och conversations/README.md
är separat infrastruktur och ingår inte i tariffdiffen. De lämnas orörda.
Batch 7:s publiceringsspärr ligger fortsatt utanför scope.

## P1 — saknad eller ogiltig behörighetsregel godtas fortfarande

`fjarrvarme.ts:137` returnerar fortfarande null vid saknad eligibility.
`besparingsvarde.ts:beraknaArsprodukt` anropar funktionen även för en
identifierad Vattenfall-profilprodukt utan att kräva en giltig regel.
Kopieringen i till_prisar lagar dagens transport men inte denna spärr.

Oberoende reproduktion med git-archive-kopia av webb-HEAD och riktig
Batch 8-generator, utan mockad motor eller handbyggd prisårsfixtur:
Uppsala Standard, 220 MWh, 100 kW abonnemang, profil 1, flödesval 0,
katalogband 1, behörighetsenergi 100 MWh och tre högsta effekt 200 kW.
Originalregeln blockerar kvot 0,5 med eligibility_not_met. Att enbart ta
bort eligibility eller sätta den till null ger i stället kostnad
**352 772 kr**, status annual/estimated/complete. Även threshold av
strängtypen "0" släpps igenom via JavaScripts typkonvertering.
Med behörighetsenergi 600 MWh godtas metric="invalid" och komplett
kostnad returneras: metric valideras inte alls.

Pythonkontrollen i katalog.py har motsvarande saknad-regel-no-op och
saknar strukturell regelvalidering. Säkerställ samma fail-closed-kontrakt
för den obligatoriska Vattenfall-vägen i båda språken. Valfria regler för
andra tariffprodukter ska inte oavsiktligt göras obligatoriska.

## P2 — bindande produktacceptans är ännu inte slutförd

Den nya isolerade sviten går igenom, men scenario 27 väljer tre profiler
och räknar sedan enbart med den sista (Industri). Scenario 28 prövar
bara Uppsala Standard. Scenario 29 prövar endast ett saknat flödesfält för
Spetsig. Detta bevisar inte verklig beräkning med alla profiler, Spetsigs
behörighetsgräns, alla tolv riktiga produkter eller mutationskraven från
014. Gröna scenarier ersätter inte dessa uttryckliga acceptanskrav.
De fem nya Pythonfallen testar transport/band, inte de i 014 begärda
regressionerna för auktoritativt behörighetsblock och snapshot-avvisning.

## Godtagna delrättningar och oberoende verifiering

- Eligibility finns nu i den verkliga genererade kandidaten: 12 poster.
- Isolerad generator anger 73 godkända katalograder; kandidaten har 75
  produktnycklar. Skarp katalog/TS är inte aktiverad. Skarpa räkningar
  86/61/63 och disposition 62/2/28 kvarstår enligt regressionsgrindarna.
  74/2/16 är fortsatt en framtida aktiveringsprojektion.
- Kapacitetsbandet härleds nu ur katalogens enda nivå; 0/2 band avvisas.
- Skarp TS ändrar enbart commit-proveniensen; a17d537 är en verklig
  skills-commit. Ingen aktiv prisårskropp ändras i denna rundas diff.
- UI visar estimated och dokumenterade exkluderingar.
- Python: **2058 passed, 4 skipped**.
- TypeScript: **2068 passed, 65 filer**, tsc --noEmit grönt.
- Isolerat bygge och verklig Batch 8-browsergrind: **29/29 gröna**.
  Första försöket kunde inte binda Vite-port i sandbox; omkörning med
  tillåten lokal server/browseråtkomst slutfördes med exit 0.
- De 26 ordinarie scenarierna ingick i kandidatgrinden. En separat ny
  körning mot skarp dist gjordes inte av Codex; leveransens 26/26 är
  Claudes rapport. Inga produktfiler eller skarp dist ändrades här.

## Nästa avgränsade steg

Claude ska inom samma scope:

1. Kräva en närvarande och strukturellt giltig eligibility-regel för
   Vattenfalls profilprodukter i båda språken: stödd metric/jämförelse,
   rätt numerisk typ och ändligt tillåtet tröskelvärde. Ogiltig/saknad
   metadata ska ge kontrollerad blockering utan kostnad, inte no-op,
   implicit typkonvertering eller okontrollerat undantag.
2. Lägga varaktiga tester genom verklig generator och produktfasad för
   samtliga tolv rader, Standard/Spetsig under/på/över 1,2 och
   saknad/null/muterad regel. Lägg även de tidigare begärda Pythonfallen
   för behörighetsblock och förkastad snapshot-omklassificering.
3. Slutföra 014:s återstående acceptans: beräkna faktiskt med alla tre
   profiler, verifiera kostnadseffekt och profilvikter/etiketter/statiska
   bindningar med mutationer; behåll exakta rabattgränser och båda sidor
   i båda språken för alla profiler. Bevisa Spetsig-gränsen i browser,
   ogiltiga fält och spärrat kr-/besparingsläge genom riktig produktväg.
   Återanvänd befintlig isolering, utan skarp aktivering eller diständring.
4. Köra full regression, isolerat bygge/browser och ordinarie regression;
   rapportera 73/75, framtida 74/2/16 och oförändrad skarp 86/61/63,
   62/2/28 samt ändrade filer och exakta slut-HEAD:ar.
5. Lägga daterad loggrättelse: 015:s påstående om skills@451e0cf med
   förälder 644407c som startpunkt beskriver 013, inte granskningscommit
   014. Faktisk leveransförälder är a17d537. Ange styrkt kontrollpunkt;
   påstå inte retroaktivt att en startkontroll utfördes utan belägg.

Verifiera produkt-HEAD:arna ovan och skills granskningscommit med
7585c57 som förälder före ändring; stoppa fail-closed vid avvikelse.
Avsluta med ny unik committad `REVIEW_READY: Codex` och stanna.
Ingen aktivering, push, historikomskrivning eller infraändring ingår.
Codex granskar/godkänner; Claude utför rättningen; agent-bridge är enbart
signaltransport. Ingen push utfördes i detta granskningssteg.
