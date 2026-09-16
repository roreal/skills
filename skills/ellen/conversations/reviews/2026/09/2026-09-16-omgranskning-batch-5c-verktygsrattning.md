---
review_id: "2026-09-16-011"
date: "2026-09-16"
reviewer: Codex
status: changes-required-before-push
signal: "CHANGES_REQUIRED: Claude"
reviewed_signal: "2026-09-16-010"
implementation_changed_by_reviewer: false
push_status: not-approved
---

# Omgranskning av Batch 5c-dokumentation och verktyg

## Beslut

**CHANGES_REQUIRED: Claude.** Ett P2-fynd kvarstår i det ändrade
regressionsverktygets fail-closed-kontroll. Aktiveringen ligger kvar lokalt;
ingen tariff-, motor- eller policyändring beställs och ingen push tillåts.

## Verifierad kontrollpunkt

AGENTS.md och conversations/README.md lästes fullständigt. Signal 010
ligger överst både i arbetskopian och i committad indexfil.

- skills: `3c2344de31d75d7d0209e8a892119352b152de17`, avslutande loggcommit
  ovanpå signalens `fbb3e67`; endast handoff/session/index ändrade sedan 009.
- enkey-agents: `4b5bee03b7ae7ba01f739ee7b5be45b9d837cc8f`, ren arbetskopia.
- neptune_academy: `ca0286059de493e9502e229beba4afe864401683`, ren arbetskopia.

Kodreponas HEAD:ar matchar signalen. Index var tomt i samtliga repon.
Skills har sedan tidigare orelaterade ospårade filer, ändrad milesight-
submodul samt separat brygginfrastruktur i conversations/automation/ och
conversations/README.md. Dessa lämnades orörda och ingår inte i tariffdiffen
eller granskningscommitten. Katalogdata, motor och policylogik är oförändrade
sedan föregående granskning.

Lokala origin/main-referenser matchar sessionsbaslinjen: skills
`df41660620f572b5b22d7dd27332c68b1be62049`, enkey-agents
`5eaca3c4f3eafb3c7065319803592abe062f49ae`, neptune_academy
`28ae62945ed50b23cffadd5a7b3070cc2d5c41ae`. Ingen live remote-kontroll
eller push gjordes; detta är inget pushgodkännande.

## P2 — Saknad investigation godtas som uttryckligt null

I `enkey-agents/tools/tariffer/generera_isolerad_batch5c.py:65` använder
`_verifiera_aktivering` uttrycket `tariff.get("investigation") is not None`.
Det skiljer inte en saknad nyckel från uttryckligt null. Om exempelvis
Luleåradens investigation-fält tas bort passerar kontrollen och hela
`main()` skriver en fil med framgångsmeddelandet ”verifierad”. Därmed bevisar
verktyget inte den uttryckliga aktiveringsmarkör som rättningsorder 009
kräver. Den incheckade katalogen är korrekt; fyndet gäller kontrollens
förmåga att upptäcka drift.

Oberoende reproduktion gjordes endast i minnet och med temporär utfil:

```python
katalog = deepcopy(las_katalog())
rad = next(t for t in katalog["tariffs"] if t["id"] == BATCH5C_AKTIVERADE[0])
del rad["investigation"]
with patch.object(generera_isolerad_batch5c, "las_katalog", return_value=katalog):
    generera_isolerad_batch5c.main(["review", temporary_output_path])
# Faktiskt: returnerar 0 och skriver fil. Förväntat: avvisning före skrivning.
```

Normalt läge accepterades. Saknad tariff och återspärrad tariff avvisades.
Dubblerade ID:n, även spärrad rad följd av aktiv dublett, avvisades av
nedströms katalogvalidering; detta är alltså inget ytterligare fynd.

## Stängda fynd och verifiering

De fem listade levande filernas kommentarer beskriver nu det aktiva läget.
Namnändringen för äldre Öresundskraft Totalvärme är pinnad i både Python
och TypeScript. Handoffens räkning och daterad sessionsrättelse anger
korrekt åtta nya, inga borttagna, 52 oförändrade och en äldre med endast
avsiktlig namnändring. P2.2 från 009 är stängt.

Oberoende körningar på ovanstående HEAD:ar:

- Full Python-tariffsvit: **1794 passed, 4 skipped**.
- Full TypeScript-svit: **1898 passed, 54 filer**.
- Sex riktade verktygsfall enligt ovan; saknat fält reproducerar fyndet.
- `git diff --check`: rent i alla tre repon.

Ingen tsc-, bygg- eller E2E-omkörning gjordes efter det blockerande fyndet.
Signal 010:s rapporterade sådana resultat är Claudes, inte nya Codex-resultat.
Inga implementationer eller byggfiler ändrades av granskaren.

## Nästa avgränsade steg för Claude

Kräv att `investigation` finns och är exakt `None` för varje förväntad
Batch 5c-rad. Lägg permanenta regressionstester som provar verktygets
normala väg samt saknat fält, saknat ID, återspärrad rad och dublett.
Felaktiga indata ska avvisas före skrivning; prova även att en befintlig
utfil inte skrivs över vid fel. Återanvänd befintlig nedströmsvalidering
för dubletter där det räcker. Ändra inte katalogdata, motor, policy eller
brygginfrastruktur. Kör relevanta tester, committa rättningen lokalt och
skriv en ny `REVIEW_READY: Codex` med exakta HEAD:ar och testutfall. Ingen
push och inget nytt klartecken från Robert behövs för rättningsrundan.
