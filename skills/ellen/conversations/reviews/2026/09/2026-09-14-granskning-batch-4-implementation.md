---
review_id: "2026-09-14-004"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 4 lokal implementation bakom spärr"
  - "skills@e8341ce (katalogcommit skills@c1d8320)"
  - "enkey-agents@69b3060"
  - "neptune_academy@289b9c0"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
---

# Granskning: Batch 4 — lokal implementation

## Beslut

**Changes required före aktivering.** Prisformlernas golden-facit, den nya
flödesdifferensmotorn, den isolerade 37-räkningen och de ordinarie testsviterna är gröna.
Fyra acceptansblockerande luckor återstår däremot i den fail-closed-kedja som ska knyta
katalog, policy, kontraktsfasad och motor till varandra. De fyra tariffspärrarna ska därför
ligga kvar och ingen push är godkänd.

Ingen tariffkod har ändrats av Codex i denna granskning.

## Fynd

### P1. Multiplikatorn saknar dubbelriktad katalog–policy–motorbindning

`till_prisar()` transporterar inte `capacity.post_multiplier` eller en normaliserad,
allow-listad markör till `prisar` (`enkey-agents/tools/tariffer/katalog.py:926-953`).
Aktiveringspreflighten anropar bara justerings-, band- och flödeskontroller
(`policyregister.py:1664-1668`) och kontrollerar därför inte det omvända fallet: en policy
med `kapacitet_multiplikator_bindning` för en tariff som inte har någon godkänd
`post_multiplier`.

Kontraktsfasaden för sedan varje sådan bindning vidare som ett tal
(`resultatkontrakt.py:1039-1057`; TypeScript `resultatkontrakt.ts:1315-1332`) och den direkta
motorn multiplicerar valfri kapacitetskostnad om värdet bara är ändligt
(`faktura.py:319-327`; TypeScript `fjarrvarme.ts:346-354`).

Codex reproducerade felet genom att lägga en syntetisk multiplikatorbindning i en
Jämtkraftpolicy. `kontrollera_aktiveringsgrind()` godkände kombinationen och den verkliga
årsfasaden halverade bandets kapacitetskostnad från **32 120 kr till 16 060 kr**. Det är en
tyst kostnadsförvanskning, inte bara ett saknat test.

Rätta genom att transportera en explicit, normaliserad och allow-listad
multiplikatordeskriptor/markör från katalogen och korsvalidera i båda riktningar:

- katalogmarkör finns om och endast om katalogen har den exakt stödda multiplikatorn;
- policybindning finns om och endast om samma markör finns;
- bindningen, fältet och intervallet hör till samma stödda form;
- markör utan bindning/värde och bindning på tariff utan markör faller stängt;
- Python- och TypeScriptmotorn försvarar sig även vid direktanrop och accepterar inte en
  multiplikator utan den godkända deskriptorn eller utanför dess tillåtna intervall.

Lägg negativa Python- och TypeScriptprov för bindning på Jämtkraft/annan tariff, markör utan
bindning eller värde, fel intervall samt direkt motorväg med otillåtet/icke-ändligt värde.

### P1. Kompositgrinden accepterar godtycklig multiplikatorstruktur

`kontrollera_kompositgrind()` säger att den verifierar exakt den enda stödda Umeåformen,
men kontrollerar i praktiken bara att `name` och `input_U` är icke-tomma strängar samt att
minst ett stycke har två icke-tomma strängar (`policyregister.py:1541-1604`). Den verifierar
inte `name="B"`, den källbundna `input_U`, de fyra exakta intervallen/formlerna eller
policyfältets exakta `[0.93, 1.401]`.

Följande okända struktur accepterades i Codex reproduktion:

```python
{
    "name": "X",
    "input_U": "anything",
    "pieces": [{"source_interval": "nonsense", "formula": "arbitrary-code-like-text"}],
}
```

Grinden ska använda en sluten, källpinnad strukturbeskrivning och avvisa fel namn,
inpututtryck, antal/delordning, intervall, formel eller extra semantik. Lägg separata
regressionstest för varje avvikelse samt de beställda andra-pass-fallen: dold okänd issue,
dold okänd justering och en framtida okänd `post_multiplier`.

### P1. Justeringsschemat validerar inte enhet eller formel

`_valid_flow_difference()` och `_valid_asymmetric_flow_difference()` verifierar tal och
månader men ignorerar både `unit` och `formula`
(`enkey-agents/tools/tariffer/justeringar.py:298-349`). Codex bytte båda fälten till
`"WRONG"`; båda validatorerna returnerade `None`. Detta strider direkt mot handoffens krav
på exakt typ, formelparametrar, enhet och månadsmängd och kan få en annan enhet eller
formelbetydelse att tolkas som SEK/m³.

Gör schemastrukturen sluten och källbunden för båda typerna. Pinna de accepterade
enheterna/formlerna och lägg negativa tester för fel eller saknade värden samt oväntade
semantiska fält. Om normaliserad metadata transporteras till TypeScript ska pariteten också
testas där.

### P1. Det beställda verkliga UI-/produktbytestestet saknas

Handoffens acceptanspunkt 8 kräver ett riktigt komponent-/E2E-prov med injicerad Jämtkraft-
och Umeåkandidat: rätt fält/enheter, normal submit och `annual/snapshot/complete`. Den kräver
också produktbyte Jämtkraft↔Umeå och mellan två Jämtkraft-ID:n. Leveransloggen bekräftar
själv att detta inte gjordes (`sessions/2026/09/2026-09-14-batch-4-jamtkraft-umea.md:176-183`).

TypeScripttestet konstruerar syntetiska `prisar` och policyer direkt; det bevisar varken den
generatorproducerade Batch 4-policyn eller `KalkylatorPage`. Särskilt viktigt är att
flödesnyckeln delas mellan fyra policyer trots handoffens order om unika nycklar. Den
nuvarande sidan ser ut att rensa policystate vid leverantörsbyte
(`KalkylatorPage.tsx:372-393`), men det ska bevisas via den verkliga UI-vägen. Antingen görs
nycklarna tariffunika eller så dokumenteras den avsiktliga avvikelsen och produktbytestestet
visar att inget gammalt flöde, effektvärde, band eller B återanvänds.

### P2. Levande verifieringsdokument motsäger implementerad proveniens och indata

- `verifieringslista-fjarrvarmebolag.md:133-147` anger fortfarande `15_0` s.18–19 som
  Jämtkraftkälla, och texten säger fortfarande att den redan ifyllda
  `billing_basis_method` måste mappas. Byt till `15_1` med verifierade sidor 19–20 och
  beskriv faktiskt lokalt läge bakom spärr.
- Samma fil, raderna 384–388, avslutas fortfarande med leverantörens **A och B/U** trots att
  kontraktet uttryckligen tar direkt A och direkt B, aldrig U. Uppdatera även datum/status
  till den genomförda officiella återverifieringen.
- Jämtkraftposterna i `tariffinventering-v22.md:804`, `:823` och `:842` samt
  `batchplan-v22.md:918-921` räknar bara effekt och flöde. Implementationen och handoffen
  kräver dessutom bekräftat band-ID: alltså tre tariffspecifika fält.
- Sessionsloggen påstår att generatorns båda `godkanda(katalog)`-anrop uttryckligen för samma
  register vidare. Byggvägen gör det på `generera.py:168`, men sluträkningen på `:284`
  använder fortfarande det implicita globala standardregistret. Antingen gör anropet
  explicit eller rätta rapportens påstående; samma register ska bevisligen användas i
  generering och kontrollräkning.

## Verifierat i granskningen

- Python fullsvit: **1259 passed, 4 skipped**; endast sandboxens kända varning om
  `.pytest_cache`.
- TypeScript fullsvit: **1194 passed**; `npx tsc --noEmit` rent.
- Riktade Batch 4-prov: **35 Python** och **17 TypeScript** passerar.
- `npm run eval:build`: grönt; endast befintlig bundelstorleksvarning.
- `git diff --check`/`git diff --cached --check`: rent i alla tre repon.
- Katalogens 86, skarp katalogmängd 33, skarp totalmängd 35, isolerad mängd 37 och
  dispositionen **33/31/28 av 92** är oförändrade.
- Den genererade filens katalog-SHA matchar katalogbytesen; diffen av den skarpa artefakten
  är bara proveniens/genereringsdatum och innehåller inga Batch 4-produkter.
- Orelaterad arbetskopiesmuts i `skills` och befintliga `neptune-marketing/dist`-ändringar är
  orörd.

Gröna happy-path-test utgör inte godkännande av de reproducerade negativa vägarna ovan.

## Rättningsordning till Claude

1. Stäng den dubbelriktade multiplikatorbindningen genom katalog → genererad deskriptor →
   policy → kontraktsfasad → motor i Python och TypeScript.
2. Gör Umeås kompositstruktur och de två flödesjusteringsschemana exakt fail-closed; lägg
   negativa manipulationstest och andra-pass-test.
3. Lägg den verkliga injicerade kandidatens UI-/E2E-prov inklusive produktbyte och verifiera
   att fel visas fältnära.
4. Synka verifieringslista, inventering, batchplan och sessionspåståenden med verklig kod.
5. Kör riktade och fulla sviter, tsc, isolerat bygge, E2E, generatorsynk, räkningsmatris och
   diffkontroll. Commitera fokuserat lokalt och stanna för Codex omgranskning.

Spärrarna, 33/31/28 och förbuden mot aktivering/push gäller oförändrat under rättningen.
