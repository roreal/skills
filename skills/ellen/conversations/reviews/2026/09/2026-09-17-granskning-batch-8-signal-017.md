---
review_id: "2026-09-17-018"
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
  skills: "8e1138eb411e1c7cf7fa26fc3fcf62ade65a77ee"
  enkey_agents: "c468ebc3d5a2abff3d721299f66db791b1c67cea"
  neptune_academy: "41dde169a789235f9ea38257196fa70fa10bde28"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av Batch 8, signal 017

## Beslut

`CHANGES_REQUIRED: Claude`. Fail-closed-rättningen för saknad/null/
feltypad eligibility och okänd metric godtas som delrättning. Aktivering
är fortsatt spärrad eftersom uttrycklig produkt- och mutationsacceptans
från 014/016 saknas. Rättningen ryms i befintligt scope och kräver inget
nytt klartecken från Robert.

## Kontrollpunkt och omfattning

AGENTS.md och conversations/README.md lästes fullständigt, liksom Ellens
SKILL.md. Committad indexfil och arbetskopia är identiska; 017 ligger
överst och förekommer exakt en gång som sessions-ID. 018 var ledigt.
HEAD:ar och arbetskopior kontrollerades igen före loggskrivning.

Skills 8e1138e har granskningscommit 2902edc (016) som förälder.
Produktcommittarna har ded969a respektive f24333e som föräldrar och
matchar leveransen. Live origin/main verifierades med git ls-remote i
alla tre repon och matchar 016. Produktarbetskopiorna är rena.

Granskad rättningsdiff: skills 2902edc..8e1138e (session/index),
enkey-agents ded969a..c468ebc (justeringar.py, katalog.py,
test_batch_8_vattenfall.py), neptune_academy f24333e..41dde16
(fjarrvarme.ts, vattenfallArsprodukt.test.ts,
besparingsvardeVattenfallProdukt.test.ts, kalkylator.smoke.mjs).
Skarp tariffer.generated.ts och dist är oförändrade i denna diff och i
arbetskopian. Befintliga skills-ändringar och ospårade filer har bevarats;
filinnehåll kontrollerades med SHA-256. Milesight-status är oförändrad.
conversations/automation/ och conversations/README.md är separat
infrastruktur, lämnas orörda och räknas inte som tariffdiff.
Batch 7:s publiceringsspärr omfattas inte av detta beslut.

## P2 — verklig TS-kandidatacceptans saknas fortfarande

besparingsvardeVattenfallProdukt.test.ts använder fortfarande vi.doMock,
ett syntetiskt tariff-ID, en handbyggd Uppsala Standard-policy och
`justeringar: []`. Inga tolv genererade riktiga prisår provas där.
Pythonproven för alla tolv rader genom fasaden är värdefulla men ersätter
inte transporten till TypeScript och webbproduktens kostnadsberäkning.
017:s påstående om samtliga tolv rader genom riktig generator/produktväg
i Python/TS är därför för brett.

## P2 — profilmutationer och rabattgränser är inte färdigbevisade

De tre nya testerna med namnet ”kostnaden matchar oktober-april-andelen”
kontrollerar bara tolv vikter och positiv, ändlig kostnad. De jämför ingen
förväntad kostnad eller säsongsandel. Profil-ID 99 är ogiltig kundindata;
det är inte ett mutationsprov av profilvikter, etiketter eller bindningar.

Oberoende reproduktion i en tillfällig git-archive-kopia av 41dde16:
byt enbart plats på viktvektorerna för Industri och Lokal i fjarrvarme.ts.
Kör vattenfallArsprodukt.test.ts och besparingsvardeVattenfallProdukt.test.ts.
**67/67 tester passerar**, trots fel bindning mellan produktval och
energiprofil. Originalarbetskopian ändrades aldrig. Detta visar konkret
varför distinkta eller positiva kostnader inte uppfyller mutationskravet.

Rabattgränstesterna i båda språken använder fortfarande flerbostadsprofilen
(0,89 säsongsandel). Kravet på exakta gränser och båda sidor för alla tre
profiler i 014/016 är inte slutfört.

## Godtagna delrättningar och oberoende verifiering

- Full Python-svit: **2150 passed, 4 skipped**.
- Full TypeScript-svit: **2082 passed, 65 filer**; tsc --noEmit grönt.
- Isolerat bygge och browser mot committad 41dde16: **29/29 gröna**,
  inklusive faktisk beräkning med tre profiler och Spetsigs gräns.
  Första försöket stoppades av sandboxens serverbindning; omkörning med
  tillåten lokal server/browseråtkomst gav exit 0.
- De 26 ordinarie scenarierna ingick i kandidatgrinden; separat ny körning
  mot skarp dist gjordes inte. 017:s separata 26/26 är Claudes rapport.
- Auktoritativt behörighetsblock och snapshot-avvisning har nu varaktiga
  Python-regressioner. Saknad/null/strängtypad regel och ogiltig metric
  blockeras av den nya valideringen i båda språken.
- Skarpa spärrar och dispositionsgrindar ingår i full Python-svit och är
  gröna: 86/61/63 och 62/2/28 består. Ingen katalogaktivering har skett.
- Daterad proveniensrättelse finns. git diff --check är rent i produktrepona.

## Nästa avgränsade steg

Claude ska slutföra befintlig acceptans, utan aktivering:

1. Återanvänd generera_isolerad_batch8.py/bygg_ts_fran_katalog och befintlig
   isolerad testkopia. Kör verkliga beraknaArsprodukt mot de tolv genererade
   prisåren med riktiga justeringar/policyer, alla tre profiler och
   Standard/Spetsig under/på/över 1,2. Mutera saknad/null/ogiltig eligibility
   och visa kontrollerad blockering utan kostnad; använd behörig kontroll
   för respektive produkt så negativprovet inte passerar av fel orsak.
2. Förankra profilernas förväntade månadsserier och kostnader i oberoende
   referensvärden. Bevisa att byte av Industri/Lokal-vikter, fel etikett
   respektive fel statisk bindning upptäcks. En grön kontroll följd av ett
   avsiktligt rött mutationsprov räcker; produktmotorn behöver inte ändras
   för att känna igen alla strukturellt giltiga men felaktiga källvikter.
3. Parametrisera rabattens exakta gränser och båda sidor i Python och TS
   för alla tre profiler och jämför rätt säsongsbelopp, inte bara kostnad > 0.
4. Behåll gröna browserprov för profilval/Standard/Spetsig/estimated/
   exkluderingar. Lägg ett negativt prov av en muterad isolerad kandidat
   samt ogiltig fältindata genom befintlig React/browserväg; kr- och
   besparingsresultat ska vara spärrade. En tunn testadapter inom befintlig
   isolering är redan tillåten enligt 014. Detta är inte brygginfrastruktur.
   En full tolv×tre×tröskel-matris i browser krävs inte: produktmatrisen
   kan köras i TS och representativa UI-fall i browser.
5. Kör full regression, isolerat bygge/browser och ordinarie regression
   utan att röra skarp dist. Rapportera isolerat 73/75, projektion 74/2/16
   och oförändrat skarpt 86/61/63, 62/2/28. Rätta 017:s alltför breda
   täckningspåstående med daterat tillägg, inte tyst omskrivning.

Verifiera produkt-HEAD:arna ovan och skills granskningscommit med 8e1138e
som förälder innan ändring; stoppa fail-closed vid avvikelse. Bevara alla
arbetskopieundantag. Avsluta med unik committad REVIEW_READY: Codex,
exakta slut-HEAD:ar och faktiska testutfall, och stanna.

Codex granskar/godkänner. Claude utför nästa rättning. agent-bridge
förmedlar endast signalen. Ingen aktivering, push eller historikomskrivning
har utförts i detta granskningssteg.
