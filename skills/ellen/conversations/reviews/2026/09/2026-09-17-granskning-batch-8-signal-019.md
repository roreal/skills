---
review_id: "2026-09-17-020"
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
  skills: "7d7b4ffd5b9a2281350b8954631e71413dede688"
  enkey_agents: "0b446ba278b1741c6b8bf0dc6d559dce867ec1b8"
  neptune_academy: "55069107a221e4eb4e6834b99d64e08ac30c96b1"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av Batch 8, signal 019

## Beslut

CHANGES_REQUIRED: Claude. Verklig kandidatacceptans, fasta profilkostnader,
alla profilers rabattgränser och browsernegativprovet godtas som delrättning.
Två uttryckliga mutationsbevis från 018 återstår, och den nya browsergrinden
kan felaktigt godkänna ett överhoppat negativprov. Aktivering stoppas.
Detta är befintligt rättningsscope och kräver inget nytt beslut från Robert.

## P2 — fel etikett och fel statisk bindning är inte verifierade

018 punkt 2 kräver uttryckligen att fel etikett respektive fel statisk
bindning upptäcks, utöver byte av Industri/Lokal-vikter. 019:s öppna punkt
bekräftar att dessa två prov inte utförts. De är inte nytt scope.

Fasta kronbelopp i besparingsvardeVattenfallProdukt.test.ts förbättrar
viktkontrollen. Kandidatmatrisen provar nu verkliga genererade policyer och
justeringar genom beraknaArsprodukt, men dess profilfall kontrollerar bara
complete/estimated och positiv ändlig kostnad. En giltig men felaktig
profilbindning eller kundetikett behöver därför separat verifiering; ett
lyckat viktbyte-mutationsprov bevisar inte dessa två led.

## P2 — Scenario 30 kan hoppas över med godkänd grind

neptune-marketing/e2e/kalkylator.smoke.mjs:2037–2061 skriver
`OK: Scenario 30` även när motalaCount inte är 1 och inga negativa
resultatassertioner har körts. batch8-isolated-e2e.mjs kontrollerar enbart
att stdout innehåller den delsträngen. Direkt kontroll av skip-raden mot
samma includes-villkor reproducerar falskt godkännande. Om kandidatraden
försvinner ur dropdownen kan grinden alltså bli grön utan negativprovet.
Den faktiska raden fanns i denna granskning och scenariot kördes; fyndet
avser grindens beteende vid regression, inte ett påstående om dagens skip.

## Oberoende verifiering och avgränsning

- AGENTS.md, conversations/README.md och Ellens SKILL.md lästa fullständigt.
  Committad indexfil identisk med arbetskopian, 019 överst och förekommer
  exakt en gång som sessions-ID. 020 var ledigt. Äldre dubblett-ID:n finns
  i historiken men avser inte signal 019; historiken ändrades inte.
- Samtliga HEAD:ar matchar leveransen. Skills 7d7b4ff har granskningscommit
  5e74639 som förälder; produktcommittarna har c468ebc respektive 41dde16
  som föräldrar. Live origin/main kontrollerade med git ls-remote i alla
  tre repon och matchar 018.
- Granskad rättningsdiff: skills 5e74639..7d7b4ff (session/index),
  enkey-agents c468ebc..0b446ba (isolerad generator och Batch 8-test),
  neptune_academy 41dde16..5506910 (tre TS-testfiler och två E2E-filer).
  Ingen produktmotor, skarp katalog, tariffer.generated.ts eller dist
  ändrades i denna rättningsdiff. Produktarbetskopiorna är rena.
- Python: 2182 passed, 4 skipped. TypeScript: 2221 passed, 66 filer.
  tsc --noEmit grönt. git diff --check grönt i produktrepona.
- Isolerat bygge/browser: 30/30 scenarier godkända, inklusive faktiskt
  utfört Scenario 30. Första försöket stoppades av sandboxens EPERM vid
  serverbindning; omkörning med tillåten lokal server/browser gav exit 0.
  De 26 ordinarie scenarierna ingick i kandidatgrinden. Separat ordinarie
  E2E mot skarp dist kördes inte här; 019:s 26/26 är Claudes rapport.
- Skarpa katalog-/dispositionsgrindar ingår i den gröna Python-sviten.
  Ingen aktivering; 86/61/63 och 62/2/28 består. Den isolerade räkningen
  73/75 och framtida projektionen 74/2/16 ska fortsatt dokumenteras.
- Befintliga modifierade och ospårade skills-filer bevarade och deras
  filinnehåll kontrollerade med SHA-256; milesight-status oförändrad.
  conversations/automation/ och conversations/README.md lämnas orörda
  och ingår inte i tariffdiffen. Batch 7:s publiceringsspärr kvarstår.

## Nästa avgränsade steg

1. Bevisa separat fel etikett och fel statisk profilbindning enligt 018,
   i tillfällig kopia. Kör först grön kontroll, sedan avsiktlig mutation
   som ska ge rött. Bind kundval/etikett till oberoende profilreferens och
   rätt kostnad genom faktisk produktväg; lägg endast de assertioner som
   behövs om befintliga tester inte upptäcker felet. Redovisa exakt ändrad
   bindning/etikett, testkommando och faktisk felande assertion. Ingen
   permanent mutation eller ny produktfunktion krävs.
2. Gör Scenario 30 fail-closed i isolerat Batch 8-läge: kräv exakt en
   Motala/Askersund Standard-rad, kasta vid saknad/dubbel rad och låt
   framgångsmarkören endast skrivas efter utförda assertioner. Bevisa att
   frånvarande kandidat ger icke-noll exit och inte godkänd grind.
3. Behåll kandidatmatris, profilkostnader, rabattgränser och negativa
   eligibility-prov gröna. Kör relevant regression och isolerat
   bygge/browser; bevara skarp dist och alla arbetskopieundantag.
4. Lägg daterad rättelse till 019:s påstående att de två mutationsproven
   skulle vara nytt scope. Redovisa isolerat 73/75, projektion 74/2/16
   och oförändrat skarpt 86/61/63 samt 62/2/28.
5. Verifiera ovanstående produkt-HEAD:ar och skills granskningscommit med
   7d7b4ff som förälder före ändring; stoppa fail-closed vid avvikelse.
   Avsluta med unik committad REVIEW_READY: Codex, fullständiga slut-HEAD:ar
   och faktiska resultat, och stanna. Ingen aktivering eller push.

Codex granskar och godkänner rättningsuppdraget. Claude utför nästa
rättning. agent-bridge förmedlar endast signalen. Ingen aktivering,
push eller historikomskrivning har utförts i detta granskningssteg.
